from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health_check'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.user_profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    
    # Interview Experience endpoints
    path('interviews/', views.interview_experience_list_create, name='interview_list_create'),
    path('interviews/<int:pk>/', views.interview_experience_detail, name='interview_detail'),
    
    # Task Experience endpoints  
    path('tasks/', views.task_experience_list_create, name='task_list_create'),
    path('tasks/<int:pk>/', views.task_experience_detail, name='task_detail'),
    
    # Public endpoints for viewing all experiences
    path('public/interviews/', views.public_interview_experiences, name='public_interviews'),
    path('public/tasks/', views.public_task_experiences, name='public_tasks'),
    path('public/users/<int:user_id>/', views.user_profile_detail, name='user_profile_detail'),
]
