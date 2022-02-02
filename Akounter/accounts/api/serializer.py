from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password

# thrid-party
from rest_framework import serializers

# custom
from accounts.models import (
    Role,
    UserRoleMap,
    UserDetail,
    User,
    UserExperience,
    UserEducation,
    Skill,
    ActivityLog,
    LoginDeviceTrack
)
from master.models import Campaign
#from helpers.views import (
    #generate_hashed_password,
    #get_user_default_permission
#)




# user list and retrieve serializer
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "password",
            "email",
            "is_active",
            "is_staff",
            "is_superuser",
            "user_permissions",
            "last_login"
        ]


# user create and update serializer
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "password",
            "email",
            "mobile"
        ]
    @property
    def custom_full_errors(self):
        """
        Returns full errors formatted as per requirements
        """
        default_errors = self.errors # default errors dict
        errors = {}
        for field_name, field_errors in default_errors.items():
            for field_error in field_errors:
                field_error_message = '%s'%(field_error)
                errors.update({field_name:field_error_message})
        return errors
    
    
    # function to create user entry
    #def create(self, validated_data):
        #user = User.objects.create(
            #username            = validated_data['username'],
            #first_name          = validated_data['first_name'],
            #last_name           = validated_data['last_name'],
            #email               = validated_data['email'],
            # password          = generate_hashed_password(validated_data['password']),
            #password            = make_password(validated_data['password']),
            #mobile              = validated_data["mobile"],
            #is_active           = True # Deactivate account till it is confirmed
        #)
        # get default permissions n set them for new user 
        #user.user_permissions.set(get_user_default_permission())

        #return user
    
    # function to update existing user entry
    #def update(self, instance, validated_data):
        #instance.username = validated_data.get('username', instance.username)
        #instance.first_name = validated_data.get('first_name', instance.first_name)
        #instance.last_name = validated_data.get('last_name', instance.last_name)
        #instance.email = validated_data.get('email', instance.email)
        #if validated_data.get('password', False):
            #instance.password = generate_hashed_password(validated_data['password'])
        #instance.user_permissions.set(validated_data.get("user_permissions", instance.user_permissions))
        #instance.save()

        #return instance

        


# role list, retrieve, create and update serializer
class RoleListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = [
            "id",
            "campaign",
            "role",
            "permissions",
            "active"
        ]


class RoleCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = [
            "role",
            "permissions"
        ]

    # fucntion to create serializer
    def create(self, validated_data):
        request = self.context['request']
        # comment this line as soon as session variables have been setup
        # request.session["company"] = 1

        role = Role.objects.create(
            campaign         = get_object_or_404(Campaign, campaign_user=request.user, active=True),
            role                = validated_data["role"],
            permissions         = validated_data["permissions"],
            active              = True,
            created_by          = request.user,
            updated_by          = request.user
        )

        return role


# User serializer for User Detail serializer to update info in nested serializers
# only for use in User Detail serializer to update info in nested serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email"
            # "mobile",
        ]
        Depth = 2
        # Use to remove validations from the field 
        extra_kwargs = {
            'email': {
                'validators': [],
            }
            # 'mobile': {
            #     'validators': [],
            # }
        }

# user detail list serializer
class UserDetailListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserDetail
        fields = [
            "id",
            "user",
            "user_detail_campaign",
            "mrn_no",
            "profile_pic",
            "profile_pic_icon",
            "cover_pic",
            "company_name",
            "alt_mobile_1",
            "alt_mobile_2",
            "alt_email_1",
            "alt_email_2",
            "home_address",
            "company_address",
            "company_phone",
            "company_city",
            "home_city",
            "company_pincode",
            "home_pincode",
            "profession",
            "status",
            "dob",
            "gender",
            "about",
            "nationality",
            "region",
            "cop"
        ]
        # depth of relationships that should be traversed
        # ex:- user is a foriegn key so if Depth is 1 then u can see all details of User table too
        depth = 1

# user detail create serializer
class UserDetailCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserDetail
        fields = [
            "user",
            "user_detail_campaign",
            "mrn_no",
            "profile_pic",
            "cover_pic",
            "company_name",
            "alt_mobile_1",
            "alt_mobile_2",
            "alt_email_1",
            "alt_email_2",
            "home_address",
            "company_address",
            "company_phone",
            "company_city",
            "home_city",
            "company_pincode",
            "home_pincode",
            "profession",
            "status",
            "dob",
            "gender",
            "about",
            "nationality",
            "region",
            "cop"
        ]

    # function to create serializer
    def create(self, validated_data):
        request = self.context['request']

        user_detail = UserDetail.objects.create(
            user                =request.user,
            user_detail_campaign=validated_data["user_detail_campaign"],
            mrn_no              =validated_data["mrn_no"],
            profile_pic         =validated_data["profile_pic"],
            cover_pic           =validated_data["cover_pic"],   
            company_name        =validated_data["company_name"],
            alt_mobile_1        =validated_data["alt_mobile_1"],
            alt_mobile_2        =validated_data["alt_mobile_2"],
            alt_email_1         =validated_data["alt_email_1"],
            alt_email_2         =validated_data["alt_email_2"],
            home_address        =validated_data["home_address"],
            company_address     =validated_data["company_address"],
            company_phone       =validated_data["company_phone"],
            company_city        =validated_data["company_city"],
            home_city           =validated_data["home_city"],
            home_pincode        =validated_data["home_pincode"],
            company_pincode     =validated_data["company_pincode"],
            profession          =validated_data["profession"],
            dob                 =validated_data["dob"],
            gender              =validated_data["gender"],
            about               =validated_data["about"],
            nationality         =validated_data["nationality"],
            region              =validated_data["region"],
            cop                 =validated_data["cop"],
            
            active              = True,
            created_by          = request.user,
            updated_by          = request.user
        )    

        return user_detail        

    
# user detial update serializer
class UserDetailUpdateSerializer(serializers.ModelSerializer):
    
    # use to update data of 2 modals in same serializer
    user = UserSerializer(many=False,partial=True)  

    class Meta:
        model = UserDetail
        fields = [
            "user",
            "user_detail_campaign",
            "mrn_no",
            # "profile_pic",
            # "cover_pic",
            "company_name",
            "alt_mobile_1",
            "alt_mobile_2",
            "alt_email_1",
            "alt_email_2",
            "home_address",
            "company_address",
            "company_phone",
            "company_city",
            "home_city",
            "home_pincode",
            "company_pincode",
            "profession",
            "status",
            "dob",
            "gender",
            "about",
            "nationality",
            "region",
            "cop"
        ]

    # update both modals (User n User Details) 
    def update(self, instance, validated_data):
        # update User fields
        user = validated_data.get('user')
        instance.user.first_name = user.get('first_name')
        instance.user.last_name = user.get('last_name')
        instance.user.email = user.get('email')
        # instance.user.mobile = user.get('mobile')
        instance.user.save()
        # update User Details fields
        instance.user_detail_campaign = validated_data.get('user_detail_campaign')
        instance.mrn_no               = validated_data.get('mrn_no')
        # instance.profile_pic          = validated_data.get('profile_pic')
        # instance.cover_pic            = validated_data.get('cover_pic')
        instance.company_name         = validated_data.get('company_name')
        instance.alt_mobile_1         = validated_data.get('alt_mobile_1')
        instance.alt_mobile_2         = validated_data.get('alt_mobile_2')
        instance.alt_email_1          = validated_data.get('alt_email_1')
        instance.alt_email_2          = validated_data.get('alt_email_2')
        instance.home_address         = validated_data.get('home_address')
        instance.company_address      = validated_data.get('company_address')
        instance.company_phone        = validated_data.get('company_phone')
        instance.company_city         = validated_data.get('company_city')
        instance.home_city            = validated_data.get('home_city')
        instance.company_pincode      = validated_data.get('company_pincode')
        instance.home_pincode         = validated_data.get('home_pincode')
        instance.profession           = validated_data.get('profession')
        instance.dob                  = validated_data.get('dob')
        instance.gender               = validated_data.get('gender')
        instance.about                = validated_data.get('about')
        instance.nationality          = validated_data.get('nationality')
        instance.region               = validated_data.get('region')
        instance.cop                  = validated_data.get('cop')
        instance.save()

        return instance    
    


# user experience list and retrieve serializer
class UserExperienceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExperience
        fields = [
            "id",
            "experience_user",
            "title",
            "employment_type",
            "company",
            "location",
            "start_date",
            "end_date",
            "description",
            "link",
            "active"
        ]
        depth = 1


# user experience create and update serializer
class UserExperienceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExperience
        fields = [
            "title",
            "employment_type",
            "company",
            "location",
            "start_date",
            "end_date",
            "description",
            "link"
        ]
    
    # function to create user experience entry
    def create(self, validated_data):
        request = self.context['request']
        userexperience = UserExperience.objects.create(
            experience_user     = request.user,
            title               = validated_data['title'],
            employment_type     = validated_data['employment_type'],
            company             = validated_data['company'],
            location            = validated_data['location'],
            start_date          = validated_data['start_date'],
            end_date            = validated_data['end_date'],
            description         = validated_data['description'],
            link                = validated_data['link'],
            
            active              = True,

            created_by          = request.user,
            updated_by          = request.user
        )

        return userexperience


# user education list and retrieve serializer
class UserEducationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEducation
        fields = [
            "id",
            "education_user",
            "school",
            "degree",
            "field_of_study",
            "start_date",
            "end_date",
            "grade",
            "activities",
            "description",
            "link",
            "active"
        ]
        depth = 1


# user education create and update serializer
class UserEducationeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEducation
        fields = [
            "school",
            "degree",
            "field_of_study",
            "start_date",
            "end_date",
            "grade",
            "activities",
            "description",
            "link"
        ]
    
    # function to create user education entry
    def create(self, validated_data):
        request = self.context['request']
        usereducation = UserEducation.objects.create(
            education_user      = request.user,
            school              = validated_data['school'],
            degree              = validated_data['degree'],
            field_of_study      = validated_data['field_of_study'],
            start_date          = validated_data['start_date'],
            end_date            = validated_data['end_date'],
            grade               = validated_data['grade'],
            activities          = validated_data['activities'],
            description         = validated_data['description'],
            link                = validated_data['link'],
            
            active              = True,

            created_by          = request.user,
            updated_by          = request.user
        )

        return usereducation


# user skills list and retrieve serializer
class UserSkillListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = [
            "id",
            "skill_user",
            "skill_name",
            "active"
        ]
        depth = 1


# user skills create and update serializer
class UserSkillCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = [
            "skill_name"
        ]
    
    # function to create user skills entry
    def create(self, validated_data):
        request = self.context['request']
        skill = Skill.objects.create(
            skill_user      = request.user,
            skill_name      = validated_data['skill_name'],
            
            active          = True,

            created_by      = request.user,
            updated_by      = request.user
        )

        return skill

# activity log list and retrieve serializer
class ActivityLogListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = [
            "id",
            "description",
            "date",
            "mode",
            "konnect_user"
                ]

# activity log list and retrieve serializer
class ActivityLogCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = [
            "description",
            "date",
            "mode",
            "konnect_user"
                ]

    def create(self, validated_data):
        request = self.context['request']

        activitylog = ActivityLog.objects.create(
            description        = validated_data['description'],
            date               = validated_data['date'],
            user               = request.user,
            mode               = validated_data['mode'],
            konnect_user       = validated_data["konnect_user"],
            active             = True,

            created_by         = request.user,
            updated_by         = request.user
        )

        return activitylog    

# UserRoleMap List serializer
class UserRoleMapListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoleMap
        fields = [
            "id",
            "user",
            "role",
            "active"
                ]
        depth = 1        

# user list and retrieve serializer
class UserListAPPSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "mobile"
        ]

# user profile pic update serializer 
class UserProfilePicUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        fields = [
            "profile_pic",
            "profile_pic_icon"
            # "user_permissions"
        ] 

# activity log desciption update serializer 
class ActivityLogUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = [
            "description"
        ]        

# login device detail list and create serializer
class LoginDeviceTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginDeviceTrack
        fields = [
            "app_version",
            "device_os",
            "os_version",
            "device_model",
            "device_name",
            "user",
            "login_token",
            "active"
        ]
        depth = 1

    # function to create login device detail entry
    def create(self, validated_data):
        request = self.context['request']
        track = LoginDeviceTrack.objects.create(
            app_version        = validated_data['app_version'],
            device_os          = validated_data['device_os'],
            os_version         = validated_data['os_version'],
            device_model       = validated_data['device_model'],
            device_name        = validated_data['device_name'],
            user               = request.user,
            login_token        = validated_data['login_token'],
            
            active              = True,

            created_by          = request.user,
            updated_by          = request.user
        )

        return track            