from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.models import Permission, ContentType
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

#from accounts.forms import CustomUserChangeForm, CustomUserCreationForm
from accounts.models import (
    Role,
    UserRoleMap,
    CustomToken,
    UserDetail,
    UserExperience,
    UserEducation,
    Skill,
    User,
    ActivityLog,
    SignupReferralCode,
    SignupReferralCodeUserMap,
    LoginDeviceTrack
)
#from helpers.views import get_username, get_role_name


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ["campaign", "role", "permissions"]


#@admin.register(UserRoleMap)
#class UserRoleMapAdmin(admin.ModelAdmin):
    #list_display = ["username", "role_name"]

    #def username(self, obj):
        #return ("%s" % get_username(obj.user_id))

    #def role_name(self, obj):
        #return ("%s" % get_role_name(obj.role_id))

    #username.short_description = 'User'
    #role_name.short_description = 'Role'


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ["name", "content_type", "codename"]


@admin.register(ContentType)
class ContentTypeAdmin(admin.ModelAdmin):
    list_display = ["app_label", "model"]


@admin.register(CustomToken)
class CustomTokenAdmin(admin.ModelAdmin):
    list_display = ["key", "user", "created"]


@admin.register(UserDetail)
class UserDetailAdmin(admin.ModelAdmin):
    list_display = ["user", "status"]


@admin.register(UserExperience)
class UserExperienceAdmin(admin.ModelAdmin):
    list_display = ["experience_user", "title"]


@admin.register(UserEducation)
class UserEducationAdmin(admin.ModelAdmin):
    list_display = ["education_user"]


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ["skill_user", "skill_name"]


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ["user"]

@admin.register(SignupReferralCode)
class SignupReferralCodeAdmin(admin.ModelAdmin):
    list_display = ["code", "count", "active"]

@admin.register(SignupReferralCodeUserMap)
class SignupReferralCodeUserMapAdmin(admin.ModelAdmin):
    list_display = ["referral_code", "user"]    
    
@admin.register(LoginDeviceTrack)
class LoginDeviceTrackAdmin(admin.ModelAdmin):
    list_display = ["user","device_name","device_model"]

class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference the removed 'username' field
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('email', 'first_name', 'last_name', 'mobile')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'mobile')}
        ),
    )
    #form = CustomUserChangeForm
    #add_form = CustomUserCreationForm
    list_display = ('username', 'email', 'mobile', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('date_joined',)

admin.site.register(User, CustomUserAdmin)
