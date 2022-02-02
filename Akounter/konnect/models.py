from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings

# custom
from master.models import (
    City,
    Profession,
    CentralizedData,
    Country,
    Region
)


class Connection(models.Model):
    from thumbnails.fields import ImageField

    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'

    GENDER = (
    (MALE,'Male'),
    (FEMALE,'Female'),
    (OTHER,'Other'),
    )
    
    parent_user             = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="parent_user", on_delete=models.CASCADE)
    source                  = models.TextField()
    mrn_no                  = models.CharField(max_length=15, blank=True,null=True)
    first_name              = models.CharField(max_length=250)
    last_name               = models.CharField(max_length=250, blank=True, null=True)
    nick_name               = models.CharField(max_length=250, blank=True, null=True)
    profile_pic             = models.ImageField(upload_to="profile-pic-connection", blank=True, null=True)
    # profile_pic_icon        = models.ImageField(upload_to="profile-pic-icon-connection", blank=True, null=True)
    profile_pic_icon        = ImageField(resize_source_to="large", upload_to="profile-pic-icon-connection", blank=True, null=True)
    mobile                  = models.CharField(max_length=20)
    email                   = models.CharField(max_length=200, blank=True, null=True)
    user                    = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="connection_user", on_delete=models.CASCADE, blank=True, null=True)
    connection_centralized  = models.ForeignKey(CentralizedData, related_name="connection_centralized", on_delete=models.CASCADE, blank=True, null=True)
    company_name            = models.CharField(max_length=100, blank=True, null=True)
    alt_mobile_1            = models.CharField(max_length=50, blank=True, null=True)
    alt_mobile_2            = models.CharField(max_length=50, blank=True, null=True)
    alt_email_1             = models.CharField(max_length=200, blank=True, null=True)
    alt_email_2             = models.CharField(max_length=200, blank=True, null=True)
    home_address            = models.TextField(blank=True, null=True)
    company_address         = models.TextField(blank=True, null=True)
    company_phone           = models.CharField(max_length=15, blank=True, null=True)
    company_city            = models.ForeignKey(City, related_name="connection_company_city", on_delete=models.CASCADE, blank=True, null=True)
    company_pincode         = models.CharField(max_length=25, blank=True, null=True)
    city                    = models.ForeignKey(City, related_name="connection_home_city", on_delete=models.CASCADE, null=True, blank=True)
    home_pincode            = models.CharField(max_length=25, blank=True, null=True)
    profession              = models.ForeignKey(Profession, on_delete=models.CASCADE, null=True, blank=True)
    status                  = models.IntegerField(default=1)
    dob                     = models.DateField(null=True, blank=True)
    # gender                  = models.CharField(_('Gender'),max_length=8,choices=GENDER,blank=True, null=True)
    gender                  = models.CharField(max_length=15, blank=True, null=True)
    about                   = models.TextField(blank=True, null=True)
    nationality             = models.ForeignKey(Country, related_name="connection_country", on_delete=models.CASCADE, null=True, blank=True)
    email_verified          = models.BooleanField(default=False)
    mobile_verified         = models.BooleanField(default=False)
    favourite               = models.BooleanField(default=False)
    notes                   = models.TextField(blank=True, null=True)
    region                  = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)
    cop                     = models.CharField(max_length=50, blank=True, null=True)
    voter                   = models.CharField(max_length=50, blank=True, null=True)
    booth_no                = models.CharField(max_length=50, blank=True, null=True)

    active                  = models.BooleanField(default=False)

    created_date            = models.DateTimeField(_("Created on"), default=timezone.now, blank=True)
    updated_date            = models.DateTimeField(_("Updated on"), default=timezone.now, blank=True)
    created_by              = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="connection_created_by", on_delete=models.CASCADE)
    updated_by              = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="connection_updated_by", on_delete=models.CASCADE)

    # def __str__(self):
    #     return "%s -> %s" % (self.first_name, self.status)
    
    class Meta:
        permissions = [
            ("view_own_connection", "Can view own connection"),
        ]


class ConnectionTemp(models.Model):

    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'

    GENDER = (
    (MALE,'Male'),
    (FEMALE,'Female'),
    (OTHER,'Other'),
    )
    
    parent_user             = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="parenttemp_user", on_delete=models.CASCADE)
    source                  = models.TextField()
    mrn_no                  = models.CharField(max_length=15, blank=True)
    first_name              = models.CharField(max_length=250)
    last_name               = models.CharField(max_length=250)
    profile_pic             = models.ImageField(upload_to="profile-pic-connectiontemp", blank=True, null=True)
    mobile                  = models.CharField(max_length=15)
    email                   = models.CharField(max_length=200, blank=True)
    user                    = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="connectiontemp_user", on_delete=models.CASCADE, blank=True, null=True)
    connection_centralized  = models.ForeignKey(CentralizedData, related_name="connectiontemp_centralized", on_delete=models.CASCADE, blank=True, null=True)
    company_name            = models.CharField(max_length=100, blank=True)
    alt_mobile_1            = models.CharField(max_length=50, blank=True)
    alt_mobile_2            = models.CharField(max_length=50, blank=True)
    alt_email_1             = models.CharField(max_length=200, blank=True)
    alt_email_2             = models.CharField(max_length=200, blank=True)
    home_address            = models.TextField(blank=True)
    company_address         = models.TextField(blank=True)
    company_phone           = models.CharField(max_length=15, blank=True)
    company_city            = models.ForeignKey(City, related_name="connectiontemp_company_city", on_delete=models.CASCADE, blank=True, null=True)
    city                    = models.ForeignKey(City, related_name="connectiontemp_home_city", on_delete=models.CASCADE, null=True, blank=True)
    profession              = models.ForeignKey(Profession, on_delete=models.CASCADE, null=True, blank=True)
    status                  = models.IntegerField(default=1)
    dob                     = models.DateField(null=True, blank=True)
    gender                  = models.CharField(_('Gender'),max_length=8,choices=GENDER,blank=True, null=True)
    about                   = models.TextField(blank=True)
    nationality             = models.ForeignKey(Country, related_name="connectiontemp_country", on_delete=models.CASCADE, null=True, blank=True)
    email_verified          = models.BooleanField(default=False)
    mobile_verified         = models.BooleanField(default=False)
    notes                   = models.TextField(blank=True)
    region                  = models.TextField(blank=True)
    cop                     = models.CharField(max_length=50, blank=True)
    voter                   = models.CharField(max_length=50, blank=True)
    booth_no                = models.CharField(max_length=50, blank=True)

    active                  = models.BooleanField(default=False)

    created_date            = models.DateTimeField(_("Created on"), default=timezone.now, blank=True)
    updated_date            = models.DateTimeField(_("Updated on"), default=timezone.now, blank=True)
    created_by              = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="connectiontemp_created_by", on_delete=models.CASCADE)
    updated_by              = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="connectiontemp_updated_by", on_delete=models.CASCADE)

    # def __str__(self):
    #     return "%s -> %s" % (self.parent_user, self.status)
    
    class Meta:
        permissions = [
            ("view_own_connectiontemp", "Can view own connection temp"),
        ]


class MeetingRecord(models.Model):

    meeting_connection  = models.ForeignKey(Connection, on_delete=models.CASCADE)
    meeting_notes       = models.TextField(blank=True)
    meeting_date        = models.DateTimeField(default=timezone.now, blank=True)
    action_items        = models.TextField(blank=True)
    attendees           = models.TextField(blank=True)
    next_action_date    = models.DateTimeField(null=True, blank=True)

    active              = models.BooleanField(default=False)

    created_date        = models.DateTimeField(_("Created on"), default=timezone.now, blank=True)
    updated_date        = models.DateTimeField(_("Updated on"), default=timezone.now, blank=True)
    created_by          = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="meetingrecord_created_by", on_delete=models.CASCADE)
    updated_by          = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="meetingrecord_updated_by", on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.meeting_connection.parent_user.username
    
    class Meta:
        permissions = [
            ("view_own_meetingrecord", "Can view own meeting record"),
        ]


class ConnectApproval(models.Model):
    centralized_data_id     = models.IntegerField()
    campaign_id             = models.CharField(max_length=50,null = True,blank=True)
    first_name              = models.CharField(max_length=250)
    last_name               = models.CharField(max_length=250,null = True,blank=True)
    mobile                  = models.CharField(max_length=20)
    name                    = models.CharField(max_length=500, blank=True)
    approval_status         = models.IntegerField()

    active                  = models.BooleanField(default=False)

    created_date            = models.DateTimeField(_("Created on"), default=timezone.now, blank=True)
    updated_date            = models.DateTimeField(_("Updated on"), default=timezone.now, blank=True)
    created_by              = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="connectapproval_created_by", on_delete=models.CASCADE)
    updated_by              = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="connectapproval_updated_by", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    class Meta:
        permissions = [
            ("view_own_connectapproval", "Can view own connect approval"),
        ]

class WassengerCronData(models.Model):
    user         = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="wassengercrondata", on_delete=models.CASCADE)
    user_list    = models.TextField(blank=True,null=True)
    message      = models.TextField(blank=True,null=True)
    auth_key     = models.TextField(blank=True,null=True)
    device_id    = models.TextField(blank=True,null=True)
    product_id   = models.TextField(blank=True,null=True)
    response     = models.TextField(blank=True,null=True)

    active       = models.BooleanField(default=True)

    created_date = models.DateTimeField(_("Created on"), default=timezone.now, blank=True)
    updated_date = models.DateTimeField(_("Updated on"), default=timezone.now, blank=True)
    created_by   = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="wassengercrondata_created_by", on_delete=models.CASCADE)
    updated_by   = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="wassengercrondata_updated_by", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
    class Meta:
        permissions = [
            ("view_own_wassengercrondata", "Can view own wassengercrondata"),
        ]        

