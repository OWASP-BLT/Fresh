from django.contrib import admin
from .models import TimeLog


@admin.register(TimeLog)
class TimeLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'github_issue_url', 'start_time', 'end_time', 'duration', 'is_active')
    list_filter = ('start_time', 'end_time', 'user')
    search_fields = ('user__username', 'github_issue_url', 'organization_url')
    readonly_fields = ('duration', 'created', 'updated')
    
    def is_active(self, obj):
        return obj.is_active
    is_active.boolean = True
    is_active.short_description = 'Active'