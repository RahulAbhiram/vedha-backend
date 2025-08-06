from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer, UserProfileSerializer, InterviewExperienceSerializer, TaskExperienceSerializer, UserDetailSerializer
from .models import CustomUser, UserProfile, InterviewExperience, TaskExperience
from django.http import HttpResponse

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Simple health check endpoint
    """
    return Response({
        'status': 'ok',
        'message': 'API is working!',
        'endpoints': [
            '/api/auth/register/',
            '/api/auth/login/',
            '/api/auth/logout/',
            '/api/auth/profile/'
        ]
    }, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Register a new user
    """
    print(f"Registration request data: {request.data}")  # Debug print
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)
    
    # Format error messages properly
    error_messages = []
    for field, errors in serializer.errors.items():
        for error in errors:
            error_messages.append(f"{field}: {error}")
    
    return Response({
        'error': '; '.join(error_messages) if error_messages else 'Validation failed'
    }, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    """
    Login user
    """
    print(f"Login request data: {request.data}")  # Debug print
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        login(request, user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)
    
    # Format error messages properly
    error_messages = []
    for field, errors in serializer.errors.items():
        for error in errors:
            error_messages.append(f"{field}: {error}")
    
    return Response({
        'error': '; '.join(error_messages) if error_messages else 'Invalid credentials'
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    """
    Logout user
    """
    try:
        request.user.auth_token.delete()
        logout(request)
        return Response({
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': 'Something went wrong'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    Get user profile
    """
    try:
        profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except UserProfile.DoesNotExist:
        return Response({
            'error': 'Profile not found'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    Update user profile
    """
    try:
        profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'profile': serializer.data,
                'message': 'Profile updated successfully'
            }, status=status.HTTP_200_OK)
        return Response({
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    except UserProfile.DoesNotExist:
        return Response({
            'error': 'Profile not found'
        }, status=status.HTTP_404_NOT_FOUND)

# Interview Experience Views
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def interview_experience_list_create(request):
    if request.method == 'GET':
        experiences = InterviewExperience.objects.filter(user=request.user)
        serializer = InterviewExperienceSerializer(experiences, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = InterviewExperienceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def interview_experience_detail(request, pk):
    try:
        experience = InterviewExperience.objects.get(pk=pk, user=request.user)
    except InterviewExperience.DoesNotExist:
        return Response({'error': 'Interview experience not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = InterviewExperienceSerializer(experience)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = InterviewExperienceSerializer(experience, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        experience.delete()
        return Response({'message': 'Interview experience deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

# Task Experience Views
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def task_experience_list_create(request):
    if request.method == 'GET':
        tasks = TaskExperience.objects.filter(user=request.user)
        serializer = TaskExperienceSerializer(tasks, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = TaskExperienceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def task_experience_detail(request, pk):
    try:
        task = TaskExperience.objects.get(pk=pk, user=request.user)
    except TaskExperience.DoesNotExist:
        return Response({'error': 'Task experience not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = TaskExperienceSerializer(task)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = TaskExperienceSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        task.delete()
        return Response({'message': 'Task experience deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

# Public Views for displaying all users' experiences
@api_view(['GET'])
@permission_classes([AllowAny])
def public_interview_experiences(request):
    """Get all interview experiences from all users (public view)"""
    experiences = InterviewExperience.objects.all()
    serializer = InterviewExperienceSerializer(experiences, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def public_task_experiences(request):
    """Get all task experiences from all users (public view)"""
    tasks = TaskExperience.objects.all()
    serializer = TaskExperienceSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def user_profile_detail(request, user_id):
    """Get detailed user profile with all their experiences"""
    try:
        user = CustomUser.objects.get(id=user_id)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

def admin_test(request):
    """Simple test view to check if Django is working"""
    return HttpResponse("""
    <html>
    <head><title>Django Test</title></head>
    <body>
        <h1>Django is Working!</h1>
        <p>Admin URL: <a href="/admin/">/admin/</a></p>
        <p>API Health: <a href="/api/auth/health/">/api/auth/health/</a></p>
    </body>
    </html>
    """)
