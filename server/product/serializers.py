from rest_framework import serializers
from .models import Product
from account.models import Account

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {
            'seller': {'write_only': True}
        }

class ProductAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {
            'seller': {'write_only': True}
        }

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        return product
    
    def validate(self, data):
        if data['quantity_in_stock'] < 0:
            raise serializers.ValidationError("Quantity in stock must be greater than or equal to 0")
        if data['price'] < 0:
            raise serializers.ValidationError("Price must be greater than or equal to 0")
        seller = data['seller']
        account_role = Account.objects.get(username=seller).role

        if account_role != 'SELLER':
            raise serializers.ValidationError("Only sellers can add products")
        
        if Product.objects.filter(seller=seller, name=data['name']).exists():
            raise serializers.ValidationError("Product already exists")

        return data
    