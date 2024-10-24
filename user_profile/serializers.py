from rest_framework import serializers
from user_profile.models import UserProfile
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['login', 'email', 'password', 'is_confirmed']  # Указываем поля, которые нужно сериализовать из модели User

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Включаем сериализатор User для получения полей login и email

    class Meta:
        model = UserProfile
        fields = ['user', 'passport_series', 'passport_number', 'first_name', 'last_name', 'middle_name', 'phone']
