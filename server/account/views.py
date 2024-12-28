from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
# from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import login, authenticate
from .models import Account
from .serializers import *

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'register':
            return RegistrationSerializer
        elif self.action == 'login':
            return LoginSerializer
        elif self.action == 'change_password':
            return PasswordChangeSerializer
        elif self.action == 'update_profile_info':
            return ProfileUpdateSerializer        
        return AccountSerializer

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                if (user.role == 'CUSTOMER'):
                    user.verified = True
                    user.save()
                return Response({
                    "status": "Success",
                    "message": "Account created successfully",
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)
            return Response({
                "status": "success",
                "message": "Login successful",
                "user": {
                    "email": user.email,
                    "profile_name": user.profile_name,
                    "role": user.role,
                    "id": user.id,
                    "verified": user.verified,
                    "phone": user.phone,
                    "address": user.address,
                    "profile_photo": user.profile_photo,
                    "user_name": user.username
                }
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "error",
            "message": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = Account.objects.get(username=serializer.validated_data['username'])
                user.set_password(serializer.validated_data['newpassword'])
                user.save()
                return Response({
                    "status": "success",
                    "message": "Password changed successfully"
                }, status=status.HTTP_200_OK)
            except Account.DoesNotExist:
                return Response({
                    "status": "error",
                    "message": "User not found"
                }, status=status.HTTP_404_NOT_FOUND)
        return Response({
            "status": "error",
            "message": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def update_profile_info(self, request):
        serializer = ProfileUpdateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = Account.objects.get(username=serializer.validated_data['username'])
                
                if 'profile_name' in serializer.validated_data and serializer.validated_data['profile_name'] != '':
                    user.profile_name = serializer.validated_data['profile_name']

                if 'address' in serializer.validated_data and serializer.validated_data['address'] != '':
                    user.address = serializer.validated_data['address']
                
                user.save()
                return Response({
                    "status": "success",
                    "message": "Profile updated successfully",
                    "user": {
                        "profile_name": user.profile_name,
                        "address": user.address
                    }
                }, status=status.HTTP_200_OK)
            except Account.DoesNotExist:
                return Response({
                    "status": "error",
                    "message": "User not found"
                }, status=status.HTTP_404_NOT_FOUND)
        return Response({
            "status": "error",
            "message": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    @action(detail=False, methods=['get'])
    def get_account(self, request, pk=None):
        user = Account.objects.get(id=pk)
        return Response({
            "email": user.email,
            "profile_name": user.profile_name,
            "role": user.role,
            "id": user.id,
            "verified": user.verified,
            "phone": user.phone,
            "address": user.address,
            "profile_photo": user.profile_photo,
        }, status=status.HTTP_200_OK)
