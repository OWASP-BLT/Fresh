from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.conf import settings


class TimeLog(models.Model):
    """Model for tracking time spent on GitHub issues."""
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='time_logs')
    github_issue_url = models.URLField(help_text='GitHub issue URL being tracked')
    organization_url = models.URLField(blank=True, null=True, help_text='Optional organization URL')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_time']
        indexes = [
            models.Index(fields=['user', 'start_time']),
            models.Index(fields=['github_issue_url']),
        ]
    
    def __str__(self):
        return f"TimeLog by {self.user.username} - {self.github_issue_url}"
    
    @property
    def is_active(self):
        """Check if this time log is currently active (not stopped)."""
        return self.end_time is None
    
    @property
    def elapsed_time(self):
        """Get the elapsed time for this log."""
        if self.end_time:
            return self.duration
        return timezone.now() - self.start_time
    
    def stop(self):
        """Stop the time log and calculate duration."""
        if not self.end_time:
            self.end_time = timezone.now()
            self.duration = self.end_time - self.start_time
            self.save()
    
    def save(self, *args, **kwargs):
        # Calculate duration if both start and end times are set
        if self.start_time and self.end_time and not self.duration:
            self.duration = self.end_time - self.start_time
        super().save(*args, **kwargs)