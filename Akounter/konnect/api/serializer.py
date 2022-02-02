from django.contrib.auth.models import User

# thrid-party
from rest_framework import serializers

# custom
from konnect.models import (
    Connection,MeetingRecord,ConnectionTemp,ConnectApproval
)
from accounts.models import (
    User
)


# user create and update serializer
class ConnectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = [
            "id",
            "mrn_no" ,              
            "first_name",          
            "last_name" ,
            "nick_name",           
            "mobile",
            "email" ,
            "profile_pic",
            "profile_pic_icon",
            "company_name",        
            "alt_mobile_1",          
            "alt_mobile_2",         
            "alt_email_1" ,        
            "alt_email_2" ,           
            "home_address" ,          
            "company_address",        
            "company_phone",           
            "company_city",
            "company_pincode",           
            "city",                  
            "home_pincode",                  
            "profession",            
            "status",               
            "dob", 
            "gender",                  
            "about",
            "nationality",
            "active",
            "notes",
            "region",
            "cop"                  
            # "user_permissions"
        ]

        depth = 1

# user create and update serializer
class ConnectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = [
            "mrn_no" ,
            "first_name",
            "last_name" ,
            "nick_name",
            "mobile",
            "email" ,
            "company_name",
            "alt_mobile_1",
            "alt_mobile_2",
            "alt_email_1" ,
            "alt_email_2" ,           
            "home_address" ,          
            "company_address",        
            "company_phone",           
            "company_city",
            "company_pincode",                             
            "city",
            "home_pincode",                  
            "profession",
            "dob",
            "gender",                   
            "about",
            "nationality",
            "notes",
            "region",
            "cop"                 
            # "user_permissions"
        ]
    
    # function to create user entry
    def create(self, validated_data):
        user_id = self.context['request']
        validated_data["mobile"] = validated_data["mobile"].replace(" ","")
        connection = Connection.objects.create(
            parent_user_id          = user_id,
            source                  = "Manual",
            mrn_no                  = validated_data["mrn_no"],
            first_name              = validated_data["first_name"],
            last_name               = validated_data["last_name"],
            nick_name               = validated_data["nick_name"],
            mobile                  = validated_data["mobile"].strip(),
            email                   = validated_data["email"],
            user                    = None,
            connection_centralized  = None,
            company_name            = validated_data["company_name"],
            alt_mobile_1            = validated_data["alt_mobile_1"],
            alt_mobile_2            = validated_data["alt_mobile_2"],
            alt_email_1             = validated_data["alt_email_1"],
            alt_email_2             = validated_data["alt_email_2"],
            home_address            = validated_data["home_address"],
            company_address         = validated_data["company_address"],
            company_phone           = validated_data["company_phone"],
            company_city            = validated_data["company_city"],
            company_pincode         = validated_data["company_pincode"],
            home_pincode            = validated_data["home_pincode"],
            city                    = validated_data["city"],
            profession              = validated_data["profession"],
            status                  = 1,
            dob                     = validated_data["dob"],
            gender                  = validated_data["gender"],
            about                   = validated_data["about"],
            nationality             = validated_data["nationality"],
            notes                   = validated_data["notes"],
            region                  = validated_data["region"],
            cop                     = validated_data["cop"],
            email_verified          = False,
            mobile_verified         = False,

            active                  = True, # Deactivate account till it is confirmed

            created_by_id           = user_id,
            updated_by_id           = user_id

        )

        return connection

# connection update serializer for mobile app 
class ConnectionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = [
            "mobile",
            "email" ,
            "notes"
            # "user_permissions"
        ]

# connection profile pic update serializer 
class ConnectionProfilePicUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = [
            "profile_pic",
            "profile_pic_icon"
            # "user_permissions"
        ]        
    
    # # function to create user entry
    # def create(self, validated_data):
    #     user_id = self.context['request']
    #     connection = Connection.objects.create(
    #         parent_user_id          = user_id,
    #         source                  = "Manual",
    #         mrn_no                  = validated_data["mrn_no"],
    #         first_name              = validated_data["first_name"],
    #         last_name               = validated_data["last_name"],
    #         mobile                  = validated_data["mobile"],
    #         email                   = validated_data["email"],
    #         user                    = None,
    #         connection_centralized  = None,
    #         company_name            = validated_data["company_name"],
    #         alt_mobile_1            = validated_data["alt_mobile_1"],
    #         alt_mobile_2            = validated_data["alt_mobile_2"],
    #         alt_email_1             = validated_data["alt_email_1"],
    #         alt_email_2             = validated_data["alt_email_2"],
    #         home_address            = validated_data["home_address"],
    #         company_address         = validated_data["company_address"],
    #         company_phone           = validated_data["company_phone"],
    #         company_city            = validated_data["company_city"],
    #         city                    = validated_data["city"],
    #         profession              = validated_data["profession"],
    #         status                  = 1,
    #         dob                     = validated_data["dob"],
    #         gender                  = validated_data["gender"],
    #         about                   = validated_data["about"],
    #         nationality             = validated_data["nationality"],
    #         notes                   = validated_data["notes"],
    #         region                  = validated_data["region"],
    #         cop                     = validated_data["cop"],
    #         email_verified          = False,
    #         mobile_verified         = False,

    #         active                  = True, # Deactivate account till it is confirmed

    #         created_by_id           = user_id,
    #         updated_by_id           = user_id

    #     )

    #     return connection
        
# meeting record list  serializer
class MeetingRecordListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingRecord
        fields = [
            "id",
            "meeting_connection" ,              
            "meeting_notes",          
            "meeting_date",          
            "action_items" ,           
            "attendees",
            "next_action_date" , 
            "active"                 
            # "user_permissions"
        ]
        depth = 1



# meeting record create  serializer
class MeetingRecordCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingRecord
        fields = [
            "meeting_connection" ,              
            "meeting_notes",          
            "meeting_date",          
            "action_items" ,           
            "attendees",
            "next_action_date" ,                  
            # "user_permissions"
        ]
    
    # function to create user entry
    def create(self, validated_data):
        user_id = self.context['request']
        meetingrecord = MeetingRecord.objects.create(
            meeting_connection    = validated_data["meeting_connection"],
            meeting_notes         = validated_data["meeting_notes"],
            meeting_date          = validated_data["meeting_date"],
            action_items          = validated_data["action_items"],
            attendees             = validated_data["attendees"],
            next_action_date      = validated_data["next_action_date"],

            active                = True, # Deactivate account till it is confirmed

            created_by_id          = user_id,
            updated_by_id          = user_id

        )

        return meetingrecord


# user create and update serializer
class ConnectionTempCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectionTemp
        fields = [
            "mrn_no" ,              
            "first_name",          
            "last_name" ,           
            "mobile",
            "email" ,
            "company_name",        
            "alt_mobile_1",          
            "alt_mobile_2",         
            "alt_email_1" ,        
            "alt_email_2" ,           
            "home_address" ,          
            "company_address",        
            "company_phone",           
            "company_city",           
            "city",                  
            "profession",                          
            "dob",
            "gender",                   
            "about",
            "nationality",
            "notes",
            "region",
            "cop"               
            # "user_permissions"
        ]
    
    # function to create user entry
    def create(self, validated_data):
        request = self.context['request']
        connectiontemp = ConnectionTemp.objects.create(
            parent_user             = request.user,
            source                  = "Manual",
            mrn_no                  = validated_data["mrn_no"],
            first_name              = validated_data["first_name"],
            last_name               = validated_data["last_name"],
            mobile                  = validated_data["mobile"],
            email                   = validated_data["email"],
            user                    = None,
            connection_centralized  = None,
            company_name            = validated_data["company_name"],
            alt_mobile_1            = validated_data["alt_mobile_1"],
            alt_mobile_2            = validated_data["alt_mobile_2"],
            alt_email_1             = validated_data["alt_email_1"],
            alt_email_2             = validated_data["alt_email_2"],
            home_address            = validated_data["home_address"],
            company_address         = validated_data["company_address"],
            company_phone           = validated_data["company_phone"],
            company_city            = validated_data["company_city"],
            city                    = validated_data["city"],
            profession              = validated_data["profession"],
            status                  = 1,
            dob                     = validated_data["dob"],
            gender                  = validated_data["gender"],
            about                   = validated_data["about"],
            nationality             = validated_data["nationality"],
            notes                   = validated_data["notes"],
            region                  = validated_data["region"],
            cop                     = validated_data["cop"],
            email_verified          = False,
            mobile_verified         = False,

            active                  = True, # Deactivate account till it is confirmed

            created_by              = request.user,
            updated_by              = request.user
        )
        return connectiontemp


# ConnectApproval list  serializer
class ConnectApprovalListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectApproval
        fields = [
            "id",
            "centralized_data_id" ,  
            "first_name",
            "last_name",
            "mobile" ,        
            "campaign_id",          
            "name",          
            "approval_status" ,           
            "active",              
            # "user_permissions"
        ]
        depth = 1



# ConnectApproval create  serializer
class ConnectApprovalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectApproval
        fields = [
            "centralized_data_id" ,              
            "campaign_id", 
            "first_name",
            "last_name",
            "mobile" ,         
            "name",                  
        ]
    
    # function to create user entry
    def create(self, validated_data):
        request = self.context['request']
        Connect = ConnectApproval.objects.create(
            centralized_data_id     = validated_data["centralized_data_id"],
            campaign_id             = validated_data["campaign_id"],
            name                    = validated_data["name"],
            first_name              = validated_data["first_name"],
            last_name               = validated_data["last_name"],
            mobile                  = validated_data["mobile"],
            approval_status         = 0,

            active                  = True, # Deactivate account till it is confirmed

            created_by              = request.user,
            updated_by              = request.user

        )

        return Connect


# user create and update serializer
class ConnectionListAPPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = [
            "id",            
            "first_name",          
            "last_name" ,           
            "mobile",         
            # "user_permissions"
        ]
        read_only_fields = fields