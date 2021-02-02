from django.contrib.auth import get_user_model
from rest_auth.serializers import LoginSerializer as RestAuthLoginSerializer
from rest_auth.registration.serializers import \
    RegisterSerializer as RestAuthRegisterSerializer
from rest_framework import serializers


User = get_user_model()


class UserLoginSerializer(RestAuthLoginSerializer):
    """Логин по username и password"""
    email = None


class UserRegisterSerializer(RestAuthRegisterSerializer):
    """Регистрация пользователя"""
    def save(self, *args, **kwargs):
        # todo: save wallet logic
        return super().save(*args, **kwargs)


class UserDetailSerializer(serializers.ModelSerializer):
    """Личные данные пользователя"""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'phone_number', 'date_of_birth', ]
