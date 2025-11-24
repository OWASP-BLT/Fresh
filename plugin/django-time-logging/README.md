# Django Time Logging

A Django plugin for tracking time spent on GitHub issues with real-time timer functionality.

## Features

- Track time spent on specific GitHub issues
- Real-time timer with live updates
- Simple AJAX-based interface with no page reloads
- Automatic duration calculation
- View time log history
- Direct integration with GitHub issues

## Requirements

- Python 3.11 or higher
- Django 4.0 or higher

## Installation

Install the plugin using pip:

```bash
pip install django-time-logging
```

Or install from source for development:

```bash
git clone https://github.com/OWASP-BLT/Fresh.git
cd Fresh/plugin/django-time-logging
pip install -e .
```

## Configuration

### Step 1: Add to Installed Apps

Add `time_logging` to your Django project's `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Add time_logging
    'time_logging',
    
    # Your other apps
]
```

### Step 2: Configure URL Routes

Include the time logging URLs in your project's `urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('time-logging/', include('time_logging.urls')),
    # Your other URL patterns
]
```

### Step 3: Run Migrations

Apply the database migrations:

```bash
python manage.py migrate time_logging
```

### Step 4: Create Base Template

The plugin requires a base template at `templates/base.html` with the following blocks:

```django
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}{% endblock %}</title>
    <meta name="description" content="{% block description %}{% endblock %}">
    <meta name="keywords" content="{% block keywords %}{% endblock %}">
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
```

## Usage

### Accessing the Time Logger

Navigate to `http://your-domain.com/time-logging/` in your browser.

### Starting a Time Log

1. Enter a valid GitHub issue URL (example: `https://github.com/owner/repo/issues/123`)
2. Click the "Start Time Log" button
3. The timer will begin tracking automatically

### Stopping a Time Log

1. Click the "Stop Time Log" button on the active timer
2. The duration will be calculated and saved automatically

### Viewing History

All completed time logs are displayed in a table showing:
- Start time
- End time
- Duration
- GitHub issue URL

## Admin Interface

Time logs can be managed through the Django admin interface at `/admin/time_logging/timelog/`.

## Dependencies

The plugin automatically installs the following dependencies:
- Django (>=4.0, <6.0)
- requests (>=2.31.0)
- python-dateutil (>=2.9.0)

Frontend dependencies are loaded via CDN:
- jQuery
- Tailwind CSS

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/OWASP-BLT/Fresh/issues
- Repository: https://github.com/OWASP-BLT/Fresh