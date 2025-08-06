from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile, InterviewExperience, TaskExperience

# Customize admin site headers
admin.site.site_header = "RECursion Admin Panel"
admin.site.site_title = "RECursion Admin"
admin.site.index_title = "Welcome to RECursion Administration"

# Simple CustomUser admin
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'created_at')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('-created_at',)

# Simple UserProfile admin
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'birth_date')
    search_fields = ('user__username', 'user__email')

@admin.register(InterviewExperience)
class InterviewExperienceAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'position', 'status', 'interview_date', 'rating', 'created_at')
    list_filter = ('status', 'difficulty', 'interview_date', 'created_at')
    search_fields = ('user__username', 'company_name', 'position', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(TaskExperience) 
class TaskExperienceAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'position', 'task_type', 'start_date', 'end_date', 'currently_working', 'created_at')
    list_filter = ('task_type', 'currently_working', 'start_date', 'created_at')
    search_fields = ('user__username', 'company_name', 'position', 'description', 'technologies_used')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
