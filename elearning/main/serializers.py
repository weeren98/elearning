from rest_framework import serializers
from .models import User, Course

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'real_name', 'user_type', 'email', 'is_student', 'is_teacher']

class CourseSerializer(serializers.ModelSerializer):
    teacher = UserSerializer()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'teacher']
