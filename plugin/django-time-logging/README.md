# Django Time Logging Plugin

A Django plugin for tracking time spent on GitHub issues with real-time timer functionality.

## Features

- **Start/Stop Time Logs**: Track time spent on specific GitHub issues
- **Real-time Timer**: Live timer updates without page refreshes
- **AJAX Forms**: Smooth user experience with no page reloads
- **Single Route**: Simple URL structure with one main endpoint
- **Duration Tracking**: Automatic calculation of time spent
- **GitHub Integration**: Links directly to GitHub issues

## Installation

1. **Install the plugin**:
   ```bash
   cd Fresh/plugin/django-time-logging
   pip install -e .
   ```

2. **Add to Django settings**:
   ```python
   INSTALLED_APPS = [
       # ... your other apps
       'time_logging',
   ]
   ```

3. **Include URLs in your main URLconf**:
   ```python
   from django.urls import path, include

   urlpatterns = [
       # ... your other URLs
       path('time-logging/', include('time_logging.urls')),
   ]
   ```

4. **Run migrations**:
   ```bash
   python manage.py makemigrations time_logging
   python manage.py migrate
   ```

## Usage

### Starting a Time Log

1. Navigate to `/time-logging/`
2. Enter a valid GitHub issue URL (e.g., `https://github.com/user/repo/issues/1`)
3. Click "Start Time Log"
4. The timer will begin automatically

### Active Time Log

- View the real-time timer showing elapsed time
- See the GitHub issue URL being worked on
- Click "Stop Time Log" to end the session

### Time Log History

- View all completed time logs in a table
- See start time, end time, duration, and GitHub issue
- Click on GitHub links to view the original issues

## Technical Details

### Single Route Architecture

The plugin uses a hybrid approach with:
- **One main route** (`/time-logging/`) that handles all operations
- **AJAX form submissions** for start/stop actions
- **JSON responses** for smooth user experience
- **No page refreshes** during timer operations

### Models

```python
class TimeLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    github_issue_url = models.URLField(max_length=500)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
```

### Real-time Timer

- JavaScript-based timer that updates every second
- Calculates elapsed time from the server-provided start time
- Continues running until the time log is stopped

### AJAX Integration

- Uses jQuery for AJAX requests
- CSRF token protection
- JSON request/response format
- Error handling with user-friendly messages

## Dependencies

- Django 3.2+
- djangorestframework (for CSRF tokens)
- jQuery (loaded from CDN)
- Tailwind CSS (loaded from CDN)

## Template Extension

The plugin expects a `base.html` template with the following blocks:
- `title`: Page title
- `description`: Meta description  
- `keywords`: Meta keywords
- `content`: Main content area

## Admin Interface

Time logs are automatically registered in Django admin for management and debugging.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if needed
5. Submit a pull request

## License

This project is open source and available under the MIT License.
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