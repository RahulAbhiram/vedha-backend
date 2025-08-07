from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from authentication.models import CustomUser, InterviewExperience, TaskExperience

class Command(BaseCommand):
    help = 'Show recent user activity from the frontend website'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=7,
            help='Number of days to look back (default: 7)',
        )
        parser.add_argument(
            '--live',
            action='store_true',
            help='Show live monitoring mode',
        )
    
    def handle(self, *args, **options):
        days = options['days']
        live_mode = options['live']
        
        now = timezone.now()
        cutoff_date = now - timedelta(days=days)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n🌐 RECursion Frontend Activity Monitor (Last {days} days)\n'
                + '=' * 60
            )
        )
        
        # Recent registrations
        new_users = CustomUser.objects.filter(created_at__gte=cutoff_date).order_by('-created_at')
        self.stdout.write(f'\n👥 NEW REGISTRATIONS ({new_users.count()}):')
        if new_users:
            for user in new_users:
                time_ago = self.time_ago(user.created_at)
                self.stdout.write(f'  • {user.username} ({user.email}) - {time_ago}')
        else:
            self.stdout.write('  No new registrations')
        
        # Recent interview experiences
        recent_interviews = InterviewExperience.objects.filter(created_at__gte=cutoff_date).order_by('-created_at')
        self.stdout.write(f'\n📝 INTERVIEW EXPERIENCES SUBMITTED ({recent_interviews.count()}):')
        if recent_interviews:
            for interview in recent_interviews:
                time_ago = self.time_ago(interview.created_at)
                status_emoji = {'selected': '✅', 'rejected': '❌', 'pending': '⏳', 'in_progress': '🔄'}.get(interview.status, '📝')
                self.stdout.write(
                    f'  • {interview.user.username}: {interview.company_name} - {interview.position} '
                    f'{status_emoji} {interview.status} - {time_ago}'
                )
        else:
            self.stdout.write('  No interview experiences submitted')
        
        # Recent task experiences
        recent_tasks = TaskExperience.objects.filter(created_at__gte=cutoff_date).order_by('-created_at')
        self.stdout.write(f'\n💼 TASK EXPERIENCES SUBMITTED ({recent_tasks.count()}):')
        if recent_tasks:
            for task in recent_tasks:
                time_ago = self.time_ago(task.created_at)
                status_emoji = '🟢' if task.currently_working else '⚫'
                self.stdout.write(
                    f'  • {task.user.username}: {task.company_name} - {task.position} '
                    f'{status_emoji} {task.task_type} - {time_ago}'
                )
        else:
            self.stdout.write('  No task experiences submitted')
        
        # Summary stats
        total_activity = new_users.count() + recent_interviews.count() + recent_tasks.count()
        self.stdout.write(f'\n📊 SUMMARY:')
        self.stdout.write(f'  Total Users: {CustomUser.objects.count()}')
        self.stdout.write(f'  Total Interviews: {InterviewExperience.objects.count()}')
        self.stdout.write(f'  Total Tasks: {TaskExperience.objects.count()}')
        self.stdout.write(f'  Recent Activity Items: {total_activity}')
        
        if live_mode:
            self.stdout.write(f'\n🔴 LIVE MODE: Run this command periodically to monitor activity')
            self.stdout.write(f'Command: python manage.py show_activity --days 1')
        
        self.stdout.write('\n' + '=' * 60)
    
    def time_ago(self, datetime_obj):
        now = timezone.now()
        diff = now - datetime_obj
        
        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "just now"
