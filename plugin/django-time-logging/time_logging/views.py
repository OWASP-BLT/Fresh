from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from .models import TimeLog
import json


@login_required
def TimeLogListView(request):
    """Main view for time logging interface with AJAX handling."""
    
    # Handle AJAX requests
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            data = json.loads(request.body)
            action = data.get('action')
            
            if action == 'start':
                github_issue_url = data.get('github_issue_url', '').strip()
                
                if not github_issue_url:
                    return JsonResponse({'success': False, 'message': 'GitHub issue URL is required.'})
                
                # Check if user already has an active time log
                active_log = TimeLog.objects.filter(user=request.user, end_time__isnull=True).first()
                if active_log:
                    return JsonResponse({'success': False, 'message': 'You already have an active time log. Please stop it first.'})
                
                # Create new time log
                time_log = TimeLog.objects.create(
                    user=request.user,
                    github_issue_url=github_issue_url
                )
                
                return JsonResponse({
                    'success': True, 
                    'message': 'Time log started successfully!',
                    'time_log_id': time_log.id,
                    'start_time': time_log.start_time.isoformat()
                })
            
            elif action == 'stop':
                time_log_id = data.get('time_log_id')
                
                try:
                    time_log = TimeLog.objects.get(id=time_log_id, user=request.user, end_time__isnull=True)
                    time_log.stop()
                    
                    return JsonResponse({
                        'success': True, 
                        'message': 'Time log stopped successfully!',
                        'duration': str(time_log.duration)
                    })
                except TimeLog.DoesNotExist:
                    return JsonResponse({'success': False, 'message': 'Time log not found or already stopped.'})
            
            else:
                return JsonResponse({'success': False, 'message': 'Invalid action.'})
                
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    # Regular GET request - render the page
    time_logs = TimeLog.objects.filter(user=request.user).order_by("-start_time")
    active_time_log = time_logs.filter(end_time__isnull=True).first()

    # Get or create token for CSRF protection in AJAX
    token, created = Token.objects.get_or_create(user=request.user)
    
    return render(
        request,
        "time_logs.html",
        {
            "time_logs": time_logs,
            "active_time_log": active_time_log,
            "token": token.key,
        },
    )
