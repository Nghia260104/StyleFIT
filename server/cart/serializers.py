from rest_framework import serializers
from .models import Cart

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["buyer", "product", "quantity"]
        
class HandleCartSerializer(serializers.ModelSerializer):
    buyer = serializers.IntegerField(required=True)
    product = serializers.IntegerField()
    quantity = serializers.IntegerField()
    
    class Meta:
        model = Cart
        fields = ["buyer", "product", "quantity"]
        
class GetCartSerializer(serializers.ModelSerializer):
    buyer = serializers.IntegerField()
    class Meta:
        model = Cart
        fields = ["buyer"]