from rest_framework import serializers
from .models import Discount
from account.models import Account

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'
        extra_kwargs = {
            'seller': {'write_only': True}
        }

class DiscountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'
        extra_kwargs = {
            'seller': {'write_only': True}
        }

    def create(self, validated_data):
        discount = Discount.objects.create(**validated_data)
        return discount
    
    def validate(self, data):
        if data['limit'] < 0:
            raise serializers.ValidationError("Limit must be greater than or equal to 0")
        seller = data['seller']
        season = data['season']
        year = data['year']
        account_role = Account.objects.get(id=seller).role
        if account_role != 'seller':
            raise serializers.ValidationError("Only sellers can create discounts")
        if Discount.objects.filter(seller=seller, season=season, year=year).exists():
            raise serializers.ValidationError("Discount already exists")
        
        return data