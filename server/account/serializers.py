from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'email', 'profile_name', 'role', 'profile_photo', 'phone', 'address', 'verified')

class RegistrationSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Account
        fields = ('email', 'password', 'profile_name', 'role', 'username')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': False},
            'profile_name': {'required': True},
            'username': {'required': True},
            'role': {'required': True},
        }

    def create(self, validated_data):
        user = Account.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            profile_name=validated_data['profile_name'],
            role=validated_data['role']
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")

        if not user.verified:
            raise serializers.ValidationError("Account not verified")

        # refresh = RefreshToken.for_user(user)
        # return {
        #     'user': user,
        #     'tokens': {
        #         'refresh': str(refresh),
        #         'access': str(refresh.access_token),
        #     }
        # }
        
        return user