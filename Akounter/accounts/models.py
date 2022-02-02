from django.db import models
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    UserManager,
    Permission
)
from django.shortcuts import get_object_or_404
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings


# third-party
from rest_framework.response import Response
import binascii
import re
import os
from full_url.grabber import RequestGrabber


# custom
from master.models import (
    State,
    City,
    Profession,
    Campaign,
    EmploymentType,
    Country,
    Region
)
from konnect.models import Connection


# overriding django user table
class User(AbstractBaseUser, PermissionsMixin):

    class Meta:
        app_label = "accounts"
        db_table = "user"
        ordering = ["date_joined"]

    username = models.CharField(_('username'), max_length=75, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, numbers and '
                    '@/./+/-/_ characters'),
        validators=[
            validators.RegexValidator(re.compile('^[\w.@+-]+$'), 
            _('Enter a valid username.'), 'invalid')
        ])
    first_name = models.CharField(_('first name'), max_length=250)
    last_name = models.CharField(_('last name'), max_length=250)
    mobile = models.CharField(_('mobile'), max_length=15, unique=True)
    email = models.EmailField(_('email address'), max_length=254, unique=True)


    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_superuser = models.BooleanField(_('superuser status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site with all the rights.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "last_name", "mobile", "email"]

    def get_full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def __unicode__(self):
        return self.email


class CustomToken(models.Model):

    """
    The default authorization token model.
    """
    key         = models.CharField(_("Key"), max_length=40, primary_key=True)
    device_id   = models.TextField()
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created     = models.DateTimeField(_("Created"), auto_now_add=True)

    class Meta:
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")

    def save(self, *args, **kwargs):
        # get token object if device already exixts else get False
        token_obj = self.validate_device()
        # if token_obj:
            # return existing token object
            # return token_obj
        if not self.key:
            # generate new token
            self.key = self.generate_key()
            # create custom token object and return the same
            super(CustomToken, self).save(*args, **kwargs)
            return get_object_or_404(CustomToken, key=self.key)

    # function to create key
    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()
    
    # function to validate if an account is already logged in from this device
    def validate_device(self):
        # check if entry with this device already exists 
        device_exists = CustomToken.objects.filter(device_id=self.device_id).exists()
        if device_exists:
            # delete the existing token
            CustomToken.objects.filter(device_id=self.device_id).delete()
            return False
            # return existing token object
            # return get_object_or_404(CustomToken, device_id=self.device_id)
        else:
            return False

    def __str__(self):
        return self.key


class Role(models.Model):

    campaign        = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    role            = models.CharField(max_length=60)
    permissions     = models.TextField(blank=True)
    
    active          = models.BooleanField(default=False)

    created_date    = models.DateTimeField(_("Created on"), default=timezone.now, blank=True)
    updated_date    = models.DateTimeField(_("Updated on"), default=timezone.now, blank=True)
    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="role_created_by", on_delete=models.CASCADE)
    updated_by      = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="role_updated_by", on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.role
    
    class Meta:
        permissions = [
            ("view_own_role", "Can view own role"),
        ]


class UserRoleMap(models.Model):

    user            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role            = models.ForeignKey(Role, on_delete=models.CASCADE)

    active          = models.BooleanField(default=False)

    created_date    = models.DateTimeField(_("Created on"), default=timezone.now, blank=True)
    updated_date    = models.DateTimeField(_("Updated on"), default=timezone.now, blank=True)
    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="userrolemap_created_by", on_delete=models.CASCADE)
    updated_by      = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="userrolemap_updated_by", on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s" % (self.user.username, self.role.role)
    
    class Meta:
        permissions = [
            ("view_own_userrolemap", "Can view own user role map"),
        ]


# model which contains more detials of a user
class UserDetail(models.Model):
    from thumbnails.fields import ImageField

    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'

    GENDER = (
    (MALE,'Male'),
    (FEMALE,'Female'),
    (OTHER,'Other'),
    )

    user                    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    user_detail_campaign    = models.ForeignKey(Campaign,on_delete=models.CASCADE, blank=True, null=True)
    mrn_no                  = models.CharField(max_length=15, blank=True, null=True)
    profile_pic             = models.ImageField(upload_to="profile-pic", blank=True, null=True)
    profile_pic_icon        = ImageField(resize_source_to="large", upload_to="profile-pic-icon", blank=True, null=True)
    cover_pic               = models.ImageField(upload_to="cover-pic", blank=True, null=True)
    company_name            = models.CharField(max_length=100, blank=True, null=True)
    alt_mobile_1            = models.CharField(max_length=50, blank=True, null=True)
    alt_mobile_2            = models.CharField(max_length=50, blank=True, null=True)
    alt_email_1             = models.CharField(max_length=200, blank=True, null=True)
    alt_email_2             = models.CharField(max_length=200, blank=True, null=True)
    home_address            = models.TextField(blank=True, null=True)
    company_address         = models.TextField(blank=True, null=True)
    company_phone           = models.CharField(max_length=15, blank=True, null=True)
    company_city            = models.ForeignKey(City, related_name="userdetail_company_city", on_delete=models.CASCADE, blank=True, null=True)
    company_pincode         = models.CharField(max_length=25, blank=True, null=True)
    home_city               = models.ForeignKey(City, related_name="userdetail_home_city", on_delete=models.CASCADE, null=True, blank=True)
    home_pincode            = models.CharField(max_length=25, blank=True, null=True)
    profession              = models.ForeignKey(Profession, on_delete=models.CASCADE,null=True, blank=True)
    status                  = models.IntegerField(default=1,null=True, blank=True)
    dob                     = models.DateField(null=True, blank=True)
    gender                  = models.CharField(_('Gender'),max_length=8,choices=GENDER,blank=True, null=True)
    about                   = models.TextField(blank=True, null=True)
    nationality             = models.ForeignKey(Country, related_name="userdetail_country", on_delete=models.CASCADE, null=True, blank=True)
    active_voter            = models.CharField(max_length=50, blank=True, null=True)
    email_verified          = models.BooleanField(default=False)
    mobile_verified         = models.BooleanField(default=False)
    region                  = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)
    cop                     = models.CharField(max_length=50, blank=True, null=True)

    active                  = models.BooleanField(default=False)

    created_date            = models.DateTimeField(_("Created on"), default=timezone.now, blank=True)
    updated_date            = models.DateTimeField(_("Updated on"), default=timezone.now, blank=True)
    created_by              = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="userdetail_created_by", on_delete=models.CASCADE)
    updated_by              = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="userdetail_updated_by", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
    class Meta:
        permissions = [
            ("view_own_userdetail", "Can view own user detail"),
        ]


class UserExperience(models.Model):

    experience_user     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title               = models.CharField(max_length=50)
    employment_type     = models.ForeignKey(EmploymentType, on_delete=models.CASCADE)
    company             = models.CharField(max_length=100)
    location            = models.ForeignKey(City, on_delete=models.CASCADE)
    start_date          = models.DateField()
    end_date            = models.DateField(null=True, blank=True)
    description         = models.TextField(blank=True)
    link                = models.TextField(blank=True)

    active              = models.BooleanField(default=False)

    created_date        = models.DateTimeField(_("Created on"), default=timezone.now, blank=True)
    updated_date        = models.DateTimeField(_("Updated on"), default=timezone.now, blank=True)
    created_by          = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="userexperience_created_by", on_delete=models.CASCADE)
    updated_by          = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="userexperience_updated_by", on_delete=models.CASCADE)

    def __str__(self):
        return self.experience_user.username

    class Meta:
        permissions = [
            ("view_own_userexperience", "Can view own user experience"),
        ]

    
class UserEducation(models.Model):

    education_user      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    school              = models.CharField(max_length=255)
    degree              = models.CharField(max_length=255)
    field_of_study      = models.CharField(max_length=255)
    start_date          = models.DateField()
    end_date            = models.DateField(null=True, blank=True)
    grade               = models.CharField(max_length=20, blank=True)
    activities          = models.TextField(blank=True)
    description         = models.TextField(blank=True)
    link                = models.TextField(blank=True)

    active              = models.BooleanField(default=False)

    created_date        = models.DateTimeField(_("Created on"), default=timezone.now, blank=True)
    updated_date        = models.DateTimeField(_("Updated on"), default=timezone.now, blank=True)
    created_by          = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="usereducation_created_by", on_delete=models.CASCADE)
    updated_by          = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="usereducation_updated_by", on_delete=models.CASCADE)

    def __str__(self):
        return self.education_user.username


class Skill(models.Model):

    skill_user          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    skill_name          = models.CharField(max_length=50)

    active              = models.BooleanField(default=False)

    created_date        = models.DateTimeField(_("Created on"), default=timezone.now, blank=True)
    updated_date        = models.DateTimeField(_("Updated on"), default=timezone.now, blank=True)
    created_by          = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="skill_created_by", on_delete=models.CASCADE)
    updated_by          = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="skill_updated_by", on_delete=models.CASCADE)

    def __str__(self):
        return self.skill_user.username

class ActivityLog(models.Model):
    
    description      = models.TextField(blank=True)
    date             = models.DateTimeField(blank=False,default=timezone.now, null=False)
    user             = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mode             = models.TextField(blank=False)
    konnect_user     = models.ForeignKey(Connection, on_delete=models.CASCADE)
    active           = models.BooleanField(default=False)
    created_date     = models.DateTimeField(_("Created on"), default=timezone.now, blank=True)
    updated_date     = models.DateTimeField(_("Updated on"), default=timezone.now, blank=True)
    created_by       = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="activitylog_created_by", on_delete=models.CASCADE)
    updated_by       = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="activitylog_updated_by", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username

# Forgot password mail send using rest password reset
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    
    # api with token link
    link = "{}?token={}".format(reverse('password_reset:reset-password-confirm'), reset_password_token.key)
    
    # get current site url 
    url_parts = RequestGrabber(instance.request)
    protocol = url_parts.protocol()
    domain = url_parts.domain()
    site_url = protocol+domain
    url = site_url+link 

    message = "Hey ,\n Here is your Password Reset link- \n" + url +"\n Click on above link to reset your Konnect app Password"

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Akounter Konnect"),
        # message:
        message,
        # from:
        "contact@izoe.in",
        # to:
        [reset_password_token.user.email]
    )          

class SignupReferralCode(models.Model):
    
    code            = models.CharField(max_length=254,blank=True, null=True, unique=True)
    count           = models.IntegerField(null=True, blank=True)
    expiry_date     = models.DateTimeField(blank=True, null=True)
    active          = models.BooleanField(default=False)
    created_date    = models.DateTimeField(_("Created on"), default=timezone.now, blank=True)
    updated_date    = models.DateTimeField(_("Updated on"), default=timezone.now, blank=True)
    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="signupreferralcode_created_by", on_delete=models.CASCADE)
    updated_by      = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="signupreferralcode_updated_by", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.code

class SignupReferralCodeUserMap(models.Model):
    
    referral_code   = models.ForeignKey(SignupReferralCode, on_delete=models.CASCADE)
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    active          = models.BooleanField(default=False)
    created_date    = models.DateTimeField(_("Created on"), default=timezone.now, blank=True)
    updated_date    = models.DateTimeField(_("Updated on"), default=timezone.now, blank=True)
    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="signupreferralcodeusermap_created_by", on_delete=models.CASCADE)
    updated_by      = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="signupreferralcodeusermap_updated_by", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username    


class LoginDeviceTrack(models.Model):
    
    app_version     = models.CharField(max_length=254,blank=True, null=True)
    device_os       = models.CharField(max_length=254,blank=True, null=True)
    os_version      = models.CharField(max_length=254,blank=True, null=True)
    device_model    = models.CharField(max_length=254,blank=True, null=True)
    device_name     = models.CharField(max_length=254,blank=True, null=True)
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    login_token     = models.CharField(max_length=254,blank=True, null=True)
    active          = models.BooleanField(default=False)
    created_date    = models.DateTimeField(_("Created on"), default=timezone.now, blank=True)
    updated_date    = models.DateTimeField(_("Updated on"), default=timezone.now, blank=True)
    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="logindevicetrack_created_by", on_delete=models.CASCADE)
    updated_by      = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="logindevicetrack_updated_by", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username  
