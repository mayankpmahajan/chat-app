from django.contrib.auth.models import User
from django.contrib.auth import login
from rest_framework import APIView
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
        if serializer.is_valid:
            user = serializer.validated_data['user']
            login(request, user)
            return Response({"message":"Login successful"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordRestSerializer(data = request.data)
        if serializer.is_valid:
            reset_url = serializer.save()
            return Response({'message': 'Password reset link sent', 'reset_url': reset_url}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)