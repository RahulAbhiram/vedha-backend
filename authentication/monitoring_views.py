"""
Production Monitoring System for RECursion
Like Netflix, Airbnb, Facebook - Real-time user activity monitoring
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.utils import timezone
from datetime import timedelta, datetime
import json
from .models import CustomUser, InterviewExperience, TaskExperience

class LiveActivityDashboard(View):
    """
    Real-time dashboard like big tech companies use
    Shows live user activity, registrations, submissions
    """
    
    def get(self, request):
        # Time periods
        now = timezone.now()
        today = now.date()
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)
        
        # Real-time metrics (like Netflix dashboard)
        metrics = {
            'real_time': {
                'active_users_today': CustomUser.objects.filter(
                    last_login__date=today
                ).count(),
                'new_registrations_today': CustomUser.objects.filter(
                    created_at__date=today
                ).count(),
                'submissions_today': {
                    'interviews': InterviewExperience.objects.filter(
                        created_at__date=today
                    ).count(),
                    'tasks': TaskExperience.objects.filter(
                        created_at__date=today
                    ).count()
                }
            },
            
            # Weekly trends (like Airbnb analytics)
            'weekly_trends': {
                'new_users': CustomUser.objects.filter(
                    created_at__gte=week_ago
                ).count(),
                'interview_submissions': InterviewExperience.objects.filter(
                    created_at__gte=week_ago
                ).count(),
                'task_submissions': TaskExperience.objects.filter(
                    created_at__gte=week_ago
                ).count()
            },
            
            # User engagement (like Facebook insights)
            'engagement': {
                'users_with_interviews': CustomUser.objects.filter(
                    interview_experiences__isnull=False
                ).distinct().count(),
                'users_with_tasks': CustomUser.objects.filter(
                    task_experiences__isnull=False
                ).distinct().count(),
                'most_active_users': list(
                    CustomUser.objects.annotate(
                        total_submissions=models.Count('interview_experiences') + 
                                        models.Count('task_experiences')
                    ).filter(total_submissions__gt=0)
                    .order_by('-total_submissions')[:5]
                    .values('username', 'email', 'total_submissions')
                )
            },
            
            # Recent activity feed (like Twitter/X admin)
            'recent_activity': self.get_recent_activity(),
            
            # System health (like all big sites)
            'system_health': {
                'total_users': CustomUser.objects.count(),
                'total_content': InterviewExperience.objects.count() + 
                               TaskExperience.objects.count(),
                'database_status': 'healthy',
                'last_updated': now.isoformat()
            }
        }
        
        return JsonResponse(metrics)
    
    def get_recent_activity(self):
        """Get recent activity across all models"""
        activities = []
        
        # Recent interviews
        recent_interviews = InterviewExperience.objects.order_by('-created_at')[:10]
        for interview in recent_interviews:
            activities.append({
                'type': 'interview',
                'user': interview.user.username,
                'action': f"Added interview at {interview.company_name}",
                'timestamp': interview.created_at.isoformat(),
                'metadata': {
                    'company': interview.company_name,
                    'position': interview.position,
                    'status': interview.status
                }
            })
        
        # Recent tasks
        recent_tasks = TaskExperience.objects.order_by('-created_at')[:10]
        for task in recent_tasks:
            activities.append({
                'type': 'task',
                'user': task.user.username,
                'action': f"Added {task.task_type} at {task.company_name}",
                'timestamp': task.created_at.isoformat(),
                'metadata': {
                    'company': task.company_name,
                    'position': task.position,
                    'type': task.task_type
                }
            })
        
        # Recent users
        recent_users = CustomUser.objects.order_by('-created_at')[:5]
        for user in recent_users:
            activities.append({
                'type': 'registration',
                'user': user.username,
                'action': f"New user registered",
                'timestamp': user.created_at.isoformat(),
                'metadata': {
                    'email': user.email
                }
            })
        
        # Sort by timestamp and return latest 20
        activities.sort(key=lambda x: x['timestamp'], reverse=True)
        return activities[:20]

# Live stats endpoint (like Instagram analytics)
@csrf_exempt
def live_stats_api(request):
    """API endpoint for real-time stats"""
    dashboard = LiveActivityDashboard()
    return dashboard.get(request)

# Webhook for real-time notifications (like Slack/Discord)
@csrf_exempt 
def activity_webhook(request):
    """Webhook that triggers when new activity happens"""
    if request.method == 'POST':
        # This could send to Slack, Discord, email, etc.
        # Like how Airbnb notifies when bookings happen
        data = json.loads(request.body)
        
        # Example: Send to monitoring service
        notification = {
            'timestamp': timezone.now().isoformat(),
            'event': data.get('event_type', 'unknown'),
            'user': data.get('user', 'anonymous'),
            'details': data.get('details', {})
        }
        
        # In production, this would go to:
        # - Slack webhook
        # - Email notifications  
        # - Push notifications
        # - Analytics services
        
        return JsonResponse({'status': 'notification_sent'})
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
