from django.contrib.auth.models import User

# thrid-party
from rest_framework import serializers

# custom
from master.models import (
    EmailSettings,
    SMSSettings,
    WhatsappSettings,
    CentralizedData
)
from accounts.models import (
    User
)

class EmailSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailSettings
        fields = [
            "id",
            "email_host",
            "email_host_user",
            "email_host_password",
            "email_port"
        ]
    
    def create(self, validated_data):
        request = self.context['request']
        emailsetting = EmailSettings.objects.create(
            user                = request.user,
            email_host          = validated_data["email_host"],
            email_host_user     = validated_data["email_host_user"],
            email_host_password = validated_data["email_host_password"],
            email_port          = validated_data["email_port"],
            active              = True,
            created_by          = request.user,
            updated_by          = request.user
        )

        return emailsetting


class SMSSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSSettings
        fields = [
            "id",
            "sender_id",
            "auth_key"
        ]
    
    def create(self, validated_data):
        request = self.context['request']
        smssetting = SMSSettings.objects.create(
            user         = request.user,
            sender_id    = validated_data["sender_id"],
            auth_key     = validated_data["auth_key"],
            active       = True,
            created_by   = request.user,
            updated_by   = request.user
        )

        return smssetting

class WhatsappSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhatsappSettings
        fields = [
            "id",
            "account_id",
            "auth_key",
            "from_phonenumber"
        ]
    
    def create(self, validated_data):
        request = self.context['request']
        whatsappsetting = WhatsappSettings.objects.create(
            user             = request.user,
            account_id       = validated_data["account_id"],
            auth_key         = validated_data["auth_key"],
            from_phonenumber = validated_data["from_phonenumber"],
            
            active           = True,
            created_by       = request.user,
            updated_by       = request.user
        )

        return whatsappsetting

# centralized data user list and retrieve serializer
class CentralizedUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CentralizedData
        fields = [
            "id",
            "mrn_no",
            "first_name",
            "last_name",
            "nick_name",
            "mobile",
            "email",
            "user",
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
            "cop",
            "active",
            ]
        depth = 1 