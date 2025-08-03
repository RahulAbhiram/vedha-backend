"""
URL configuration for recursion_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse, JsonResponse

def home_view(request):
    return HttpResponse("""
    <html>
    <head><title>RECursion Backend</title></head>
    <body>
        <h1>RECursion Backend API</h1>
        <ul>
            <li><a href="/admin/">Django Admin Panel</a></li>
            <li><a href="/api/auth/health/">API Health Check</a></li>
            <li><a href="/api/auth/register/">User Registration</a></li>
            <li><a href="/api/auth/login/">User Login</a></li>
        </ul>
        <p>Backend is working! ✅</p>
    </body>
    </html>
    """)

def create_superuser_view(request):
    """Temporary view to create superuser - REMOVE AFTER USE"""
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    if User.objects.filter(username='admin').exists():
        return JsonResponse({'message': 'Superuser already exists'})
    
    try:
        User.objects.create_superuser(
            username='admin',
            email='admin@recursion.com', 
            password='recursion123'
        )
        return JsonResponse({
            'message': 'Superuser created successfully!',
            'admin_url': 'https://web-production-aaeaf.up.railway.app/admin/',
            'username': 'admin',
            'password': 'recursion123'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)})

def check_admin_view(request):
    """Check admin user details for debugging"""
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    try:
        admin_user = User.objects.get(username='admin')
        return JsonResponse({
            'username': admin_user.username,
            'email': admin_user.email,
            'is_superuser': admin_user.is_superuser,
            'is_staff': admin_user.is_staff,
            'is_active': admin_user.is_active,
            'message': 'Admin user found',
            'login_hint': 'Try username: admin, password: recursion123'
        })
    except User.DoesNotExist:
        return JsonResponse({'error': 'Admin user not found'})

def reset_admin_view(request):
    """Reset admin password"""
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    try:
        admin_user = User.objects.get(username='admin')
        admin_user.set_password('recursion123')
        admin_user.is_superuser = True
        admin_user.is_staff = True
        admin_user.is_active = True
        admin_user.save()
        return JsonResponse({
            'message': 'Admin password reset successfully',
            'username': 'admin',
            'password': 'recursion123'
        })
    except User.DoesNotExist:
        # Create new admin if doesn't exist
        User.objects.create_superuser('admin', 'admin@recursion.com', 'recursion123')
        return JsonResponse({
            'message': 'Admin user created successfully',
            'username': 'admin',
            'password': 'recursion123'
        })

urlpatterns = [
    path('', home_view, name='home'),
    path('check-admin/', check_admin_view, name='check_admin'),
    path('reset-admin/', reset_admin_view, name='reset_admin'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
]
