from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.URLField(blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"

class InterviewExperience(models.Model):
    INTERVIEW_STATUS_CHOICES = [
        ('selected', 'Selected'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='interview_experiences')
    company_name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    interview_date = models.DateField()
    status = models.CharField(max_length=20, choices=INTERVIEW_STATUS_CHOICES, default='pending')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    duration = models.CharField(max_length=50, blank=True)  # e.g., "2 hours", "45 minutes"
    rounds = models.IntegerField(default=1)
    description = models.TextField()
    technical_questions = models.TextField(blank=True)
    hr_questions = models.TextField(blank=True)
    tips = models.TextField(blank=True)
    rating = models.IntegerField(default=5, help_text="Rate your experience from 1 to 5")
    salary_offered = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.company_name} - {self.position}"

class TaskExperience(models.Model):
    TASK_TYPE_CHOICES = [
        ('project', 'Project'),
        ('internship', 'Internship'),
        ('freelance', 'Freelance'),
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='task_experiences')
    company_name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    task_type = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES, default='project')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    currently_working = models.BooleanField(default=False)
    description = models.TextField()
    technologies_used = models.TextField(help_text="Technologies/tools used (comma separated)")
    achievements = models.TextField(blank=True)
    key_responsibilities = models.TextField(blank=True)
    project_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.company_name} - {self.position}"
