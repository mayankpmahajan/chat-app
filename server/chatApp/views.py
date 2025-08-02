from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import login
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from .serializers import SignUpSerializer, LoginSerializer, PasswordRestSerializer


class SignUpView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permissions_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response({"message":"Login successful"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordRestSerializer(data = request.data)
        if serializer.is_valid():
            reset_url = serializer.save()
            return Response({'message': 'Password reset link sent', 'reset_url': reset_url}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class PasswordResetConfirmView(APIView):
    def post(self, request):
        uid = request.data.get("uid")
        token = request.data.get("token")
        new_password = request.data.get("new_password")
        print("this is token", token)

        try:
            user = User.objects.get(pk=uid)
            print(user)
        except User.DoesNotExist:
            return Response({"error": "Invalid user"}, status=400)

        if default_token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password reset successful"})
        else:
            return Response({"error": "Invalid or expired token"}, status=400)