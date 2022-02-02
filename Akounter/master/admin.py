from django.contrib import admin
from django.contrib.auth.models import Permission, ContentType

from master.models import (
    State,
    City,
    Profession,
    Country,
    Campaign,
    EmailSettings,
    SMSSettings,
    EmploymentType,
    CentralizedData,
    UserDefaultPermission,
    Notification,
    WhatsappSettings,
    Region,
    AppVesrionTrack,
    VersionControl,
    ElectionMaster,
    BoothMaster,
    BoothAssociateMap
)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ["country_name", "country_abbr"]


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ["state_name", "state_abbr", "state_country"]


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ["city_name", "city_state"]


@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):
    list_display = ["profession_name"]


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ["campaign_user", "campaign_name"]


@admin.register(EmailSettings)
class EmailSettingsAdmin(admin.ModelAdmin):
    list_display = ["user"]


@admin.register(SMSSettings)
class SMSSettingsAdmin(admin.ModelAdmin):
    list_display = ["user"]


@admin.register(WhatsappSettings)
class WhatsappSettingsAdmin(admin.ModelAdmin):
    list_display = ["user"]


@admin.register(EmploymentType)
class EmploymentTypeAdmin(admin.ModelAdmin):
    list_display = ["employment_type_name"]


@admin.register(CentralizedData)
class CentralizedDataAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "mobile", "email", "mrn_no"]


@admin.register(UserDefaultPermission)
class UserDefaultPermissionAdmin(admin.ModelAdmin):
    list_display = ["default_permission"]

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["user","message","is_read"]    

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ["region","profession"]  

@admin.register(AppVesrionTrack)
class AppVesrionTrackAdmin(admin.ModelAdmin):
    list_display = ["device","version"]  

@admin.register(VersionControl)
class VersionControlAdmin(admin.ModelAdmin):
    list_display = ["city","region"]  

@admin.register(ElectionMaster)
class ElectionMasterAdmin(admin.ModelAdmin):
    list_display = ["name","region"]  

@admin.register(BoothMaster)
class BoothMasterAdmin(admin.ModelAdmin):
    list_display = ["Name","Address"]  

@admin.register(BoothAssociateMap)
class BoothAssociateMapAdmin(admin.ModelAdmin):
    list_display = ["booth","user"]      
    
