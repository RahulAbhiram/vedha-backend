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

def debug_admin_view(request):
    """Debug admin user status"""
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    try:
        admin_user = User.objects.get(username='admin')
        return JsonResponse({
            'exists': True,
            'username': admin_user.username,
            'email': admin_user.email,
            'is_superuser': admin_user.is_superuser,
            'is_staff': admin_user.is_staff,
            'is_active': admin_user.is_active,
            'has_usable_password': admin_user.has_usable_password(),
        })
    except User.DoesNotExist:
        return JsonResponse({'exists': False, 'error': 'Admin user not found'})

def recreate_admin_view(request):
    """Recreate admin user if needed"""
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    # Delete existing admin if exists
    User.objects.filter(username='admin').delete()
    
    # Create new admin
    admin_user = User.objects.create_superuser(
        username='admin',
        email='admin@recursion.com',
        password='recursion123'
    )
    
    return JsonResponse({
        'message': 'Admin user recreated successfully',
        'username': 'admin',
        'password': 'recursion123',
        'is_superuser': admin_user.is_superuser,
        'is_staff': admin_user.is_staff,
        'is_active': admin_user.is_active,
    })

urlpatterns = [
    path('', home_view, name='home'),
    path('debug-admin/', debug_admin_view, name='debug_admin'),
    path('recreate-admin/', recreate_admin_view, name='recreate_admin'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
]
