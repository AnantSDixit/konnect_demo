from django.contrib import admin
from tags.models import (
    Tag,
    DropDownTag,
    MentionTag
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["meeting_connection_id", "tag_value"]


@admin.register(DropDownTag)
class DropDownTagAdmin(admin.ModelAdmin):
    list_display = ["dd_tag_name", "dd_tag_user", "dd_tag_value"]


@admin.register(MentionTag)
class MentionTagAdmin(admin.ModelAdmin):
    list_display = ["mention_tag_name", "mention_tag_table", "mention_tag_column"]
