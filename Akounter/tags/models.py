from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings

# custom
from konnect.models import Connection


class Tag(models.Model):

    rel_type                = models.CharField(max_length=100)
    rel_id                  = models.IntegerField(null=True, blank=True)
    reference_id            = models.IntegerField(null=True, blank=True)
    meeting_connection_id   = models.ForeignKey(Connection, related_name="tag_meeting_connection", on_delete=models.CASCADE)
    tag_value               = models.CharField(max_length=200)
    tag_description         = models.TextField(null=True, blank=True)

    active                  = models.BooleanField(default=False)

    created_date            = models.DateTimeField(_("Created on"), default=timezone.now, blank=True)
    updated_date            = models.DateTimeField(_("Updated on"), default=timezone.now, blank=True)
    created_by              = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="tag_created_by", on_delete=models.CASCADE)
    updated_by              = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="tag_updated_by", on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s" % (self.tag_value, self.meeting_connection_id)

    class Meta:
        permissions = [
            ("view_own_tag", "Can view own tag"),
        ]


class DropDownTag(models.Model):

    dd_tag_name             = models.CharField(max_length=100)
    dd_tag_user             = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dd_tag_value            = models.TextField()
    dd_default_tag_value    = models.TextField()

    active                  = models.BooleanField(default=False)

    created_date            = models.DateTimeField(_("Created on"), default=timezone.now, blank=True)
    updated_date            = models.DateTimeField(_("Updated on"), default=timezone.now, blank=True)
    created_by              = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="dropdowntag_created_by", on_delete=models.CASCADE)
    updated_by              = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="dropdowntag_updated_by", on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s" % (self.dd_tag_name, self.dd_tag_user)

    class Meta:
        permissions = [
            ("view_own_dropdowntag", "Can view own dropdown tag"),
        ]


class MentionTag(models.Model):

    mention_tag_name          = models.CharField(max_length=100)
    mention_tag_table         = models.CharField(max_length=100)
    mention_tag_column        = models.TextField()

    active                    = models.BooleanField(default=False)

    created_date              = models.DateTimeField(_("Created on"), default=timezone.now, blank=True)
    updated_date              = models.DateTimeField(_("Updated on"), default=timezone.now, blank=True)
    created_by                = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="mentiontag_created_by", on_delete=models.CASCADE)
    updated_by                = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="mentiontag_updated_by", on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s - %s" % (self.mention_tag_name, self.mention_tag_table, self.mention_tag_column)

    class Meta:
        permissions = [
            ("view_own_mentiontag", "Can view own mention tag"),
        ]
