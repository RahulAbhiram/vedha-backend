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

# Debug endpoints removed for security

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
]
