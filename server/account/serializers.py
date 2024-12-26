from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('email', 'password', 'profile_name', 'role')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {
                'error_messages': {
                    'unique': 'Email already exists'
                }
            }
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        account = Account(**validated_data)
        account.set_password(password)
        account.save()
        return account
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        try:
            account = Account.objects.get(email=email)
        except Account.DoesNotExist:
            raise serializers.ValidationError("Account not found")

        if not account.verified:
            raise serializers.ValidationError("Account not verified")
            
        if not check_password(password, account.password):
            raise serializers.ValidationError("Invalid password")
            
        return {'email': email, 'role': account.role}
    
    