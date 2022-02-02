from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import Permission
from django.conf import settings


class Country(models.Model):

    country_name    = models.CharField(max_length=50)
    country_abbr    = models.CharField(blank=True,max_length=10)

    active          = models.BooleanField(default=False)

    created_date    = models.DateTimeField(_("Created on"), default=timezone.now, blank=True)
    updated_date    = models.DateTimeField(_("Updated on"), default=timezone.now, blank=True)
    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="country_created_by", on_delete=models.CASCADE)
    updated_by      = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="country_updated_by", on_delete=models.CASCADE)

    def __str__(self):
        return self.country_name
    
    class Meta:
        permissions = [
            ("view_own_country", "Can view own country"),
        ]


class State(models.Model):

    state_country   = models.ForeignKey(Country,on_delete=models.CASCADE)
    state_name      = models.CharField(max_length=50)
    state_abbr      = models.CharField(max_length=10, blank=True)

    active          = models.BooleanField(default=False)

    created_date    = models.DateTimeField(_("Created on"), default=timezone.now, blank=True)
    updated_date    = models.DateTimeField(_("Updated on"), default=timezone.now, blank=True)
    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="state_created_by", on_delete=models.CASCADE)
    updated_by      = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="state_updated_by", on_delete=models.CASCADE)

    def __str__(self):
        return self.state_name
    
    class Meta:
        permissions = [
            ("view_own_state", "Can view own state"),
        ]


class City(models.Model):

    city_name       = models.CharField(max_length=50)
    city_abbr       = models.CharField(max_length=10, blank=True)
    city_state      = models.ForeignKey(State, on_delete=models.CASCADE)

    active          = models.BooleanField(default=False)

    created_date    = models.DateTimeField(_("Created on"), default=timezone.now, blank=True)
    updated_date    = models.DateTimeField(_("Updated on"), default=timezone.now, blank=True)
    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="city_created_by", on_delete=models.CASCADE)
    updated_by      = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="city_updated_by", on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s" % (self.city_state, self.city_name)
    
    class Meta:
        permissions = [
            ("view_own_city", "Can view own city"),
        ]

class Profession(models.Model):

    profession_name = models.CharField(max_length=50)
    description     = models.TextField(blank=True)
    
    active          = models.BooleanField(default=False)

    created_date    = models.DateTimeField(_("Created on"), default=timezone.now, blank=True)
    updated_date    = models.DateTimeField(_("Updated on"), default=timezone.now, blank=True)
    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="profession_created_by", on_delete=models.CASCADE)
    updated_by      = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="profession_updated_by", on_delete=models.CASCADE)

    def __str__(self):
        return self.profession_name
    
    class Meta:
        permissions = [
            ("view_own_profession", "Can view own profession"),
        ]


class Campaign(models.Model):

    campaign_user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    campaign_id         = models.CharField(max_length=100)
    campaign_name       = models.CharField(max_length=100)
    campaign_detail     = models.TextField(blank=True)
    campaign_logo       = models.ImageField(upload_to="campaign-logo", blank=True)
    campaign_tagline    = models.TextField(blank=True)
    office_address      = models.TextField(blank=True)
    office_contact_1    = models.CharField(max_length=15, blank=True)
    office_contact_2    = models.CharField(max_length=15, blank=True)
    office_email        = models.CharField(max_length=200, blank=True)
    
    active              = models.BooleanField(default=False)

    created_date        = models.DateTimeField(_("Created on"), default=timezone.now, blank=True)
    updated_date        = models.DateTimeField(_("Updated on"), default=timezone.now, blank=True)
    created_by          = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="campaign_created_by", on_delete=models.CASCADE)
    updated_by          = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="campaign_updated_by", on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s" % (self.campaign_name, self.campaign_user)
    
    class Meta:
        permissions = [
            ("view_own_campaign", "Can view own campaign"),
        ]


class EmailSettings(models.Model):

    user                = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email_host          = models.CharField(max_length=50)
    email_host_user     = models.CharField(max_length=200)
    email_host_password = models.CharField(max_length=50)
    email_port          = models.IntegerField()

    active              = models.BooleanField(default=False)

    created_date        = models.DateTimeField(_("Created on"), default=timezone.now, blank=True)
    updated_date        = models.DateTimeField(_("Updated on"), default=timezone.now, blank=True)
    created_by          = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="emailsetting_created_by", on_delete=models.CASCADE)
    updated_by          = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="emailsetting_updated_by", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        permissions = [
            ("view_own_emailsettings", "Can view own Email Settings"),
        ]    


class SMSSettings(models.Model):

    user            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sender_id       = models.CharField(max_length=50)
    auth_key        = models.CharField(max_length=200)

    active          = models.BooleanField(default=False)

    created_date    = models.DateTimeField(_("Created on"), default=timezone.now, blank=True)
    updated_date    = models.DateTimeField(_("Updated on"), default=timezone.now, blank=True)
    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="smssetting_created_by", on_delete=models.CASCADE)
    updated_by      = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="smssetting_updated_by", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        permissions = [
            ("view_own_smssettings", "Can view own Sms Settings"),
        ]    


class WhatsappSettings(models.Model):
    TYPE_CHOICES = (
    ('wassenger','WASSENGER'),
    ('maytapi', 'MAYTAPI'),
    ('wapp', 'WAPP')
    )

    user                = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    account_id          = models.CharField(max_length=50)
    auth_key            = models.CharField(max_length=200)
    product_id          = models.CharField(max_length=200, null=True, blank=True)
    from_phonenumber    = models.CharField(max_length=200)
    type                = models.CharField(max_length=200, choices=TYPE_CHOICES, default='wassenger', null=True, blank=True)

    active              = models.BooleanField(default=False)

    created_date        = models.DateTimeField(_("Created on"), default=timezone.now, blank=True)
    updated_date        = models.DateTimeField(_("Updated on"), default=timezone.now, blank=True)
    created_by          = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="whatsappsetting_created_by", on_delete=models.CASCADE)
    updated_by          = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="whatsappsetting_updated_by", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        permissions = [
            ("view_own_whatsappsettings", "Can view own Whatsapp Settings"),
        ]  
    

class EmploymentType(models.Model):

    employment_type_name        = models.CharField(max_length=100)

    active                      = models.BooleanField(default=False)

    created_date                = models.DateTimeField(_("Created on"), default=timezone.now, blank=True)
    updated_date                = models.DateTimeField(_("Updated on"), default=timezone.now, blank=True)
    created_by                  = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="employmenttype_created_by", on_delete=models.CASCADE)
    updated_by                  = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="employmenttype_updated_by", on_delete=models.CASCADE)

    def __str__(self):
        return self.employment_type_name

class Region(models.Model):

    profession	    = models.ForeignKey(Profession, on_delete=models.CASCADE)
    region          = models.CharField(max_length=250, null=True, blank=True)

    active          = models.BooleanField(default=True)

    created_date    = models.DateTimeField(_("Created on"), default=timezone.now, blank=True)
    updated_date    = models.DateTimeField(_("Updated on"), default=timezone.now, blank=True)
    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="region_created_by", on_delete=models.CASCADE)
    updated_by      = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="region_updated_by", on_delete=models.CASCADE)

    def __str__(self):
        return self.region    

# Create your models here.
class ElectionMaster(models.Model):

    name                        = models.CharField(max_length=250,null=True,blank=True)
    description                 = models.TextField(blank=True,null=True)

    Booth_activeflag            = models.BooleanField(default=False)
    Booth_displayflag           = models.BooleanField(default=False)
    Voting_screen_displayflag   = models.BooleanField(default=False)
    profession                  = models.ForeignKey(Profession, on_delete=models.CASCADE,null=True, blank=True)
    region                      = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)


    active                      = models.BooleanField(default=False)

    created_date                = models.DateTimeField(_("Created on"), default=timezone.now, blank=True)
    updated_date                = models.DateTimeField(_("Updated on"), default=timezone.now, blank=True)
    created_by                  = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="electionmaster_created_by", on_delete=models.CASCADE)
    updated_by                  = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="electionmaster_updated_by", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    class Meta:
        permissions = [
            ("view_own_electionmaster", "Can view own election master"),
        ]

# Create your models here.
class BoothMaster(models.Model):

    election                    = models.ForeignKey(ElectionMaster, on_delete=models.CASCADE,null=True, blank=True)
    Name                        = models.CharField(max_length=250,null=True,blank=True)
    DisplayName                 = models.CharField(max_length=250,null=True,blank=True)
    
    Address                     = models.TextField(blank=True,null=True)
    city                        = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    pincode                     = models.CharField(max_length=250,null=True,blank=True)
    location_link               = models.CharField(max_length=250,null=True,blank=True)
    update_time                 = models.DateTimeField(("Update Time"), blank=True,null=True)

    active                      = models.BooleanField(default=False)

    created_date                = models.DateTimeField(_("Created on"), default=timezone.now, blank=True)
    updated_date                = models.DateTimeField(_("Updated on"), default=timezone.now, blank=True)
    created_by                  = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="boothmaster_created_by", on_delete=models.CASCADE)
    updated_by                  = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="boothmaster_updated_by", on_delete=models.CASCADE)

    def __str__(self):
        return self.Name
    
    class Meta:
        permissions = [
            ("view_own_boothmaster", "Can view own booth master"),
        ]        

# Create your models here.
class BoothAssociateMap(models.Model):

    booth                       = models.ForeignKey(BoothMaster, on_delete=models.CASCADE,null=True, blank=True)
    user                        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    active                      = models.BooleanField(default=False)

    created_date                = models.DateTimeField(_("Created on"), default=timezone.now, blank=True)
    updated_date                = models.DateTimeField(_("Updated on"), default=timezone.now, blank=True)
    created_by                  = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="boothassociatemap_created_by", on_delete=models.CASCADE)
    updated_by                  = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="boothassociatemap_updated_by", on_delete=models.CASCADE)

    def __str__(self):
        return self.booth.Name
    
    class Meta:
        permissions = [
            ("view_own_boothassociatemap", "Can view own booth associate map"),
        ]                               

class CentralizedData(models.Model):

    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'

    GENDER = (
    (MALE,'Male'),
    (FEMALE,'Female'),
    (OTHER,'Other'),
    )

    mrn_no                  = models.CharField(max_length=15, blank=True)
    first_name	            = models.TextField()
    last_name               = models.TextField()
    nick_name	            = models.TextField(blank=True, null=True)
    profile_pic             = models.ImageField(upload_to="profile-pic-centralized", blank=True, null=True)
    mobile	                = models.CharField(max_length=100)
    email	                = models.CharField(max_length=200, blank=True)
    user	                = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    company_name            = models.CharField(max_length=100, blank=True)
    alt_mobile_1	        = models.TextField(blank=True)
    alt_mobile_2	        = models.TextField(blank=True)
    alt_email_1	            = models.TextField(blank=True)
    alt_email_2	            = models.TextField(blank=True)
    home_address            = models.TextField(blank=True)
    company_address         = models.TextField(blank=True)
    company_phone           = models.CharField(max_length=15, blank=True)
    company_city            = models.ForeignKey(City, related_name="centralizeddata_company_city", on_delete=models.CASCADE, blank=True, null=True)
    company_pincode         = models.CharField(max_length=25, blank=True, null=True)        
    home_city	            = models.ForeignKey(City, related_name="centralizeddata_home_city", on_delete=models.CASCADE, null=True, blank=True)
    home_pincode            = models.CharField(max_length=25, blank=True, null=True)
    profession	            = models.ForeignKey(Profession, on_delete=models.CASCADE)
    status	                = models.IntegerField(default=1)
    dob                     = models.DateField(blank=True, null=True)
    gender                  = models.CharField(_('Gender'),max_length=8,choices=GENDER,blank=True, null=True)
    about                   = models.TextField(blank=True)
    nationality             = models.ForeignKey(Country, related_name="centralizeddata_country", on_delete=models.CASCADE, null=True, blank=True)
    email_verified          = models.BooleanField(default=False)
    mobile_verified         = models.BooleanField(default=False)
    region                  = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)
    cop                     = models.CharField(max_length=50, blank=True)
    voter                   = models.CharField(max_length=50, blank=True)
    voted                   = models.BooleanField(default=False, blank=True, null=True)
    booth_no                = models.ForeignKey(BoothMaster, on_delete=models.CASCADE,null=True, blank=True)
    vote_datetime           = models.DateTimeField(_("Vote Datetime"), blank=True, null=True)
    associate_flag          = models.CharField(max_length=100, blank=True, null=True)
    associate_year          = models.IntegerField(blank=True, null=True)
    fellowship_year         = models.IntegerField(blank=True, null=True)

    active                  = models.BooleanField(default=False)

    created_date            = models.DateTimeField(_("Created on"), default=timezone.now, blank=True)
    updated_date            = models.DateTimeField(_("Updated on"), default=timezone.now, blank=True)
    created_by              = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="centralizeddata_created_by", on_delete=models.CASCADE)
    updated_by              = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="centralizeddata_updated_by", on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s - %s" % (self.first_name, self.last_name, self.mobile)

    class Meta:
        permissions = [
            ("view_own_centralizeddata", "Can view own Centralized Data"),
        ]    


class UserDefaultPermission(models.Model):

    default_permission      = models.ForeignKey(Permission, on_delete=models.CASCADE)

    active                  = models.BooleanField(default=False)

    created_date            = models.DateTimeField(_("Created on"), default=timezone.now, blank=True)
    updated_date            = models.DateTimeField(_("Updated on"), default=timezone.now, blank=True)
    created_by              = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="userdefaultpermission_created_by", on_delete=models.CASCADE)
    updated_by              = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="userdefaultpermission_updated_by", on_delete=models.CASCADE)

    def __str__(self):
        return self.default_permission.name
    
    class Meta:
        permissions = [
            ("view_own_userdefaultpermission", "Can view own user default permission"),
        ]

class Notification(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,  null=True, blank=True)
    message = models.TextField(blank=True)
    # module_type = models.CharField(max_length=255, blank=True, null=True)
    redirect_link = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)
    is_read = models.BooleanField(default=False)
    created_date = models.DateTimeField(_("Created on"), auto_now_add=True)
    updated_date = models.DateTimeField(_("Updated on"), auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='notification_created_by',  on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='notification_updated_by',  on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.user.username
		        
class CustomPermission(models.Model):

    active                  = models.BooleanField(default=False)

    created_date            = models.DateTimeField(_("Created on"), default=timezone.now, blank=True)
    updated_date            = models.DateTimeField(_("Updated on"), default=timezone.now, blank=True)
    created_by              = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="custompermission_created_by", on_delete=models.CASCADE)
    updated_by              = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="custompermission_updated_by", on_delete=models.CASCADE)

    def __str__(self):
        return self.active
    
    class Meta:
        permissions = [
            ("add_bulkuploadconnection_custompermission", "Can Bulk Upload Connections"),
            ("add_tableexport_custompermission", "Can Export Table"),
            ("add_matchconnectswithcentral_custompermission", "Can Match Connects With CentralData"),
            ("add_shareconnects_custompermission", "Can Share Connects With Others"),
            ("add_voterandboothinfo_custompermission", "Can Vew voter & Booth Info"),
            ("add_votertrack_custompermission", "Can Track Voter"),
            ("add_advancereports_custompermission", "Can View Advance Reports & Analytics"),
            ("add_report_custompermission", "Can View Reports"),
            # ("add_approvesharedbulkconnection_custompermission", "Can Approve Shared Bulk Upload Connections"),
            ("add_sharedbulkconnection_custompermission", "Can Shared Bulk Upload Connections")
        ]                

class Feedback(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,  null=True, blank=True)
    message = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    # is_read = models.BooleanField(default=False)
    created_date = models.DateTimeField(_("Created on"), auto_now_add=True)
    updated_date = models.DateTimeField(_("Updated on"), auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='feedback_created_by',  on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='feedback_updated_by',  on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username


class AppVesrionTrack(models.Model):

    device = models.CharField(max_length=255, blank=True, null=True)
    version = models.CharField(max_length=255, blank=True, null=True)
    usual_update = models.BooleanField(default=False)
    force_update = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    # is_read = models.BooleanField(default=False)
    created_date = models.DateTimeField(_("Created on"), auto_now_add=True)
    updated_date = models.DateTimeField(_("Updated on"), auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='appvesriontrack_created_by',  on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='appvesriontrack_updated_by',  on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.version  




class VersionControl(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,  null=True, blank=True)
    city            = models.BooleanField(default=True)
    profession      = models.BooleanField(default=True)
    region          = models.BooleanField(default=True)
    country         = models.BooleanField(default=True)
    dropdown_tag    = models.BooleanField(default=True)

    active          = models.BooleanField(default=True)
    # is_read = models.BooleanField(default=False)
    created_date    = models.DateTimeField(_("Created on"), auto_now_add=True)
    updated_date    = models.DateTimeField(_("Updated on"), auto_now_add=True)
    created_by      = models.ForeignKey(
                        settings.AUTH_USER_MODEL, related_name='version_created_by',  on_delete=models.SET_NULL, null=True, blank=True)
    updated_by      = models.ForeignKey(
                        settings.AUTH_USER_MODEL, related_name='version_updated_by',  on_delete=models.SET_NULL, null=True, blank=True)

