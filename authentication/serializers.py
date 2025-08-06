from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser, UserProfile, InterviewExperience, TaskExperience

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirmPassword = serializers.CharField(write_only=True, source='confirm_password')
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'confirmPassword', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
        }
    
    def validate(self, attrs):
        confirm_password = attrs.pop('confirm_password', None)
        if attrs['password'] != confirm_password:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user)
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials.')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Must include email and password.')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'created_at')
        read_only_fields = ('id', 'created_at')

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ('user', 'bio', 'location', 'birth_date', 'avatar')

class InterviewExperienceSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = InterviewExperience
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

class TaskExperienceSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = TaskExperience
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

class UserDetailSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    interview_experiences = InterviewExperienceSerializer(many=True, read_only=True)
    task_experiences = TaskExperienceSerializer(many=True, read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'profile', 'interview_experiences', 'task_experiences', 'created_at')
        read_only_fields = ('id', 'created_at')
