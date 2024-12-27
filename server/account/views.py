from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import login
from .models import Account
from .serializers import *

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    # authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'register':
            return RegistrationSerializer
        elif self.action == 'login':
            return LoginSerializer
        return None

    # def get_permissions(self):
    #     if self.action in ['register', 'login']:
    #         return [AllowAny()]
    #     return [IsAuthenticated()]

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
        # if serializer.is_valid():
        #     return Response({
        #         "message": "Login successful",
        #         "email": serializer.validated_data['user'].email,
        #         "role": serializer.validated_data['user'].role,
        #         "tokens": serializer.validated_data['tokens']
        #     }, status=status.HTTP_200_OK)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
                }
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "error",
            "message": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)