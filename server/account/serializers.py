from rest_framework import serializers
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