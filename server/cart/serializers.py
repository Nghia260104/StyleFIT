from rest_framework import serializers
from .models import Cart
from account.models import Account

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
        extra_kwargs = {
            'buyer': {'write_only': True}
        }