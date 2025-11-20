from django.apps import AppConfig


class TimeLoggingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'time_logging'
    verbose_name = 'Time Logging'
    
    def ready(self):
        """Initialize the app when Django starts."""
        pass