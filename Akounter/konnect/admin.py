from django.contrib import admin
from konnect.models import (
    Connection,
    MeetingRecord,
    ConnectionTemp,
    ConnectApproval,
    WassengerCronData
)


@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = ["parent_user", "source", "status"]

@admin.register(WassengerCronData)
class WassengerCronDataAdmin(admin.ModelAdmin):
    list_display = ["user","created_date"]

@admin.register(MeetingRecord)
class MeetingRecordAdmin(admin.ModelAdmin):
    list_display = ["meeting_connection", "next_action_date"]

@admin.register(ConnectionTemp)
class ConnectionTempAdmin(admin.ModelAdmin):
    list_display = ["parent_user", "source", "status"]

@admin.register(ConnectApproval)
class ConnectApprovalAdmin(admin.ModelAdmin):
    list_display = ["campaign_id"]
