from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from utils.env import get_env_variable

class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6),

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid username or password")
        if not user.is_active:
            raise serializers.ValidationError("User is deactivated")
        data['user'] = user
        return data
    
class PasswordRestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email = value).exists():
            raise serializers.ValidationError("User with this email does not exist")
        return value
    
    def save(self):
        user = User.objects.get(email = self.validated_dataa['email'])
        token = default_token_generator.make_token(user)
        uid = user.pk
        FRONTEND_URL = get_env_variable("FRONTEND_URL")
        reset_url = f"{FRONTEND_URL}/reset-password/{uid}/token"

        send_mail(
            subject="Reset your password",
            message=f"Click to reset: {reset_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return reset_url