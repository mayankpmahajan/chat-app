from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from utils.env import get_env_variable
import resend

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

    class Meta:
        model = User
        fields = ['username', 'password']

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
        user = User.objects.get(email = self.validated_data['email'])
        print(user)
        token = default_token_generator.make_token(user)
        print(token)
        uid = user.pk
        FRONTEND_URL = get_env_variable("FRONTEND_URL")
        RESEND_API_KEY = "re_E6LqXrZs_C255K2BkjsnAg4huEi73fTKJ"
        reset_url = f"{FRONTEND_URL}/reset-password/{uid}/{token}"

        resend.api_key = RESEND_API_KEY

        params: resend.Emails.SendParams = {
            "from": "Acme <onboarding@resend.dev>",
            "to": ["mayank9178@gmail.com"],
            "subject": f"Reset your password, {user.username}",
            "html": f"""<strong>Hello {user.username},</strong><br/><br/>
                    Click <a href="{reset_url}">here</a> to reset your password.""",
        }

        print(params)
        email = resend.Emails.send(params)
        print(email)

        return reset_url