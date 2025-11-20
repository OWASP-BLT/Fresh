# Django Time Logging

A lightweight Django plugin for tracking time spent on GitHub issues. Perfect for developers who want to monitor their productivity and track time spent on specific development tasks.

## Features

- 🕒 Track time spent on GitHub issues
- 📊 Start/stop time logging with simple interface  
- 🔗 Link time logs to specific GitHub issues
- 🏢 Optional organization URL tracking
- ⚡ RESTful API for programmatic access
- 📱 Clean, responsive web interface

## Quick Start

### Installation

```bash
pip install django-time-logging
```

### Django Settings

Add `time_logging` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ... your other apps
    'time_logging',
    'rest_framework',  # Required for API functionality
]
```

### URL Configuration

Include the time logging URLs in your project:

```python
from django.urls import path, include

urlpatterns = [
    # ... your other patterns
    path('time-logs/', include('time_logging.urls')),
]
```

### Database Migration

Run migrations to create the necessary tables:

```bash
python manage.py makemigrations time_logging
python manage.py migrate
```

## Usage

1. Navigate to `/time-logs/` in your Django application
2. Enter a GitHub issue URL (e.g., `https://github.com/user/repo/issues/123`)
3. Optionally add an organization URL
4. Click "Start Time Log" to begin tracking
5. Click "Stop Time Log" when finished

## API Endpoints

- `POST /time-logs/api/start/` - Start a new time log
- `POST /time-logs/api/<id>/stop/` - Stop an existing time log
- `GET /time-logs/api/` - List all time logs

## License

MIT License - see LICENSE file for details.