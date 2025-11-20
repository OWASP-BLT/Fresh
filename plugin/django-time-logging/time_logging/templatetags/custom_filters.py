from django import template
from datetime import timedelta

register = template.Library()


@register.filter
def format_duration(duration):
    """Format a timedelta object into human-readable format."""
    if not isinstance(duration, timedelta):
        return "0h 0m 0s"
    
    total_seconds = int(duration.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    return f"{hours}h {minutes}m {seconds}s"


@register.filter
def before_dot(value):
    """Get the part before the first dot in a string."""
    if value and isinstance(value, str):
        return value.split('.')[0]
    return value