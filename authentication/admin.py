from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib.admin import AdminSite
from django.shortcuts import render
from django.urls import path
from django.http import JsonResponse
from .models import CustomUser, UserProfile, InterviewExperience, TaskExperience

# Custom Admin Site with Dashboard
class RECursionAdminSite(AdminSite):
    site_header = "RECursion Global Administration"
    site_title = "RECursion Global Admin"
    index_title = "🌐 RECursion Dashboard - Monitor All User Activity"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard-stats/', self.admin_view(self.dashboard_stats), name='dashboard_stats'),
        ]
        return custom_urls + urls
    
    def dashboard_stats(self, request):
        from django.utils import timezone
        from datetime import timedelta
        
        now = timezone.now()
        today = now.date()
        week_ago = now - timedelta(days=7)
        
        stats = {
            'total_users': CustomUser.objects.count(),
            'new_users_today': CustomUser.objects.filter(created_at__date=today).count(),
            'new_users_week': CustomUser.objects.filter(created_at__gte=week_ago).count(),
            'total_interviews': InterviewExperience.objects.count(),
            'interviews_today': InterviewExperience.objects.filter(created_at__date=today).count(),
            'interviews_week': InterviewExperience.objects.filter(created_at__gte=week_ago).count(),
            'total_tasks': TaskExperience.objects.count(),
            'tasks_today': TaskExperience.objects.filter(created_at__date=today).count(),
            'tasks_week': TaskExperience.objects.filter(created_at__gte=week_ago).count(),
        }
        return JsonResponse(stats)

# Use custom admin site
admin_site = RECursionAdminSite(name='recursion_admin')

# Customize admin site headers
admin.site.site_header = "RECursion Global Administration"
admin.site.site_title = "RECursion Global Admin"
admin.site.index_title = "🌐 RECursion Dashboard - Monitor All User Activity"

# Enhanced CustomUser admin with activity tracking
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'user_activity', 'created_at')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-created_at',)
    
    def user_activity(self, obj):
        interview_count = obj.interview_experiences.count()
        task_count = obj.task_experiences.count()
        return format_html(
            '<span style="color: {};">📝 {} interviews | 💼 {} tasks</span>',
            'green' if (interview_count + task_count) > 0 else 'red',
            interview_count,
            task_count
        )
    user_activity.short_description = 'Activity Summary'

# Enhanced UserProfile admin
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'birth_date', 'profile_completeness')
    search_fields = ('user__username', 'user__email', 'location')
    list_filter = ('birth_date',)
    
    def profile_completeness(self, obj):
        completed_fields = 0
        total_fields = 4
        if obj.bio: completed_fields += 1
        if obj.location: completed_fields += 1
        if obj.birth_date: completed_fields += 1
        if obj.avatar: completed_fields += 1
        
        percentage = (completed_fields / total_fields) * 100
        color = 'green' if percentage >= 75 else 'orange' if percentage >= 50 else 'red'
        return format_html(
            '<span style="color: {};">{}% complete</span>',
            color,
            int(percentage)
        )
    profile_completeness.short_description = 'Profile Status'

# Enhanced Interview Experience admin with real-time monitoring
@admin.register(InterviewExperience)
class InterviewExperienceAdmin(admin.ModelAdmin):
    list_display = ('user_link', 'company_name', 'position', 'status_badge', 'difficulty_badge', 'interview_date', 'rating_stars', 'time_since_created')
    list_filter = ('status', 'difficulty', 'interview_date', 'created_at', 'rating')
    search_fields = ('user__username', 'user__email', 'company_name', 'position', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    
    def user_link(self, obj):
        url = reverse('admin:authentication_customuser_change', args=[obj.user.pk])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = 'User'
    
    def status_badge(self, obj):
        colors = {
            'selected': 'green',
            'rejected': 'red', 
            'pending': 'orange',
            'in_progress': 'blue'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 6px; border-radius: 3px;">{}</span>',
            colors.get(obj.status, 'gray'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def difficulty_badge(self, obj):
        colors = {'easy': 'green', 'medium': 'orange', 'hard': 'red'}
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.difficulty, 'gray'),
            obj.get_difficulty_display().upper()
        )
    difficulty_badge.short_description = 'Difficulty'
    
    def rating_stars(self, obj):
        stars = '⭐' * obj.rating + '☆' * (5 - obj.rating)
        return format_html('<span title="Rating: {}/5">{}</span>', obj.rating, stars)
    rating_stars.short_description = 'Rating'
    
    def time_since_created(self, obj):
        from django.utils import timezone
        from datetime import timedelta
        
        now = timezone.now()
        diff = now - obj.created_at
        
        if diff.days > 0:
            return f"{diff.days} days ago"
        elif diff.seconds > 3600:
            return f"{diff.seconds // 3600} hours ago"
        elif diff.seconds > 60:
            return f"{diff.seconds // 60} minutes ago"
        else:
            return "Just now"
    time_since_created.short_description = 'Submitted'

# Enhanced Task Experience admin with activity monitoring
@admin.register(TaskExperience) 
class TaskExperienceAdmin(admin.ModelAdmin):
    list_display = ('user_link', 'company_name', 'position', 'task_type_badge', 'employment_status', 'duration_info', 'tech_preview', 'time_since_created')
    list_filter = ('task_type', 'currently_working', 'start_date', 'created_at')
    search_fields = ('user__username', 'user__email', 'company_name', 'position', 'description', 'technologies_used')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    
    def user_link(self, obj):
        url = reverse('admin:authentication_customuser_change', args=[obj.user.pk])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = 'User'
    
    def task_type_badge(self, obj):
        colors = {
            'project': 'blue',
            'internship': 'green',
            'freelance': 'purple',
            'full_time': 'orange',
            'part_time': 'teal'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;">{}</span>',
            colors.get(obj.task_type, 'gray'),
            obj.get_task_type_display()
        )
    task_type_badge.short_description = 'Type'
    
    def employment_status(self, obj):
        if obj.currently_working:
            return format_html('<span style="color: green; font-weight: bold;">🟢 Currently Working</span>')
        else:
            return format_html('<span style="color: gray;">⚫ Completed</span>')
    employment_status.short_description = 'Status'
    
    def duration_info(self, obj):
        if obj.currently_working:
            return f"Started: {obj.start_date}"
        elif obj.end_date:
            duration = obj.end_date - obj.start_date
            return f"{duration.days} days"
        else:
            return "No end date"
    duration_info.short_description = 'Duration'
    
    def tech_preview(self, obj):
        techs = obj.technologies_used.split(',')[:3] if obj.technologies_used else []
        preview = ', '.join([tech.strip() for tech in techs])
        if len(techs) >= 3 and len(obj.technologies_used.split(',')) > 3:
            preview += '...'
        return preview or 'No technologies listed'
    tech_preview.short_description = 'Technologies'
    
    def time_since_created(self, obj):
        from django.utils import timezone
        
        now = timezone.now()
        diff = now - obj.created_at
        
        if diff.days > 0:
            return f"{diff.days} days ago"
        elif diff.seconds > 3600:
            return f"{diff.seconds // 3600} hours ago"
        elif diff.seconds > 60:
            return f"{diff.seconds // 60} minutes ago"
        else:
            return "Just now"
    time_since_created.short_description = 'Submitted'
