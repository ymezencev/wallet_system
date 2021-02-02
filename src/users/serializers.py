from django.contrib.auth import get_user_model
from rest_auth.serializers import LoginSerializer as RestAuthLoginSerializer
from rest_framework import serializers

User = get_user_model()


class UserLoginSerializer(RestAuthLoginSerializer):
    """Логин по username и password"""
    email = None


class UserDetailSerializer(serializers.ModelSerializer):
    """Личные данные пользователя"""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'phone_number', 'date_of_birth', ]
