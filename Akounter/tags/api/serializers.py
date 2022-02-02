from django.contrib.auth.models import User

# thrid-party
from rest_framework import serializers

# custom
from tags.models import (
    Tag,
    DropDownTag,
)
from accounts.models import (
    User
)


# tag serializer for list and retrieve
class TagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            "id",
            "rel_type",
            "rel_id",
            "reference_id",
            "meeting_connection_id",
            "tag_value",
            "tag_description",
            "active"
        ]
        depth = 1


# tag create serializer
class TagCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            "rel_type",
            "rel_id",
            "reference_id",
            "meeting_connection_id",
            "tag_description",
            "tag_value"
        ]
    
    # function to create tag entry
    def create(self, validated_data):
        user = self.context['request']

        tag = Tag.objects.create(
            rel_type                = validated_data['rel_type'],
            rel_id                  = validated_data['rel_id'],
            reference_id            = validated_data['reference_id'],
            meeting_connection_id   = validated_data['meeting_connection_id'],
            tag_value               = validated_data['tag_value'],
            tag_description         = validated_data['tag_description'],

            active                  = True,

            created_by_id           = user,
            updated_by_id           = user
        )

        return tag



# dropdowntag serializer for list and retrieve
class DropDownTagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DropDownTag
        fields = [
            "id",
            "dd_tag_name",
            "dd_tag_user",
            "dd_tag_value",
            "dd_default_tag_value",
            "active"
        ]
        depth = 1


# tag create serializer
class DropDownTagCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DropDownTag
        fields = [
            "dd_tag_name",
            "dd_tag_value",
            "dd_default_tag_value"
        ]
    
    # function to create tag entry
    def create(self, validated_data):
        user = self.context['request']

        tag = DropDownTag.objects.create(
            dd_tag_name             = validated_data['dd_tag_name'],
            dd_tag_user_id          = user,
            dd_tag_value            = validated_data['dd_tag_value'],
            dd_default_tag_value    = validated_data['dd_default_tag_value'],

            active                  = True,

            created_by_id           = user,
            updated_by_id           = user
        )

        return tag