from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        
class CreateOrderSerializer(serializers.ModelSerializer):
    buyer = serializers.IntegerField(required=True)
    product = serializers.ListField(child=serializers.IntegerField(), allow_empty = True)
    quantity = serializers.ListField(child=serializers.IntegerField(), allow_empty = True)
    discount = serializers.IntegerField(required=False)
    
    class Meta:
        model = Order
        fields = ["buyer", "product", "quantity", "discount"]
        
        
class UpdateOrderSerializer(serializers.ModelSerializer):
    account = serializers.IntegerField(required=True)
    order = serializers.IntegerField(required=True)
    status = serializers.ChoiceField(choices=[
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled')
    ])
    
    class Meta:
        model = Order
        fields = ["account", "order", "status"]
        
class GetOrderSerializer(serializers.ModelSerializer):
    buyer = serializers.IntegerField()
    order = serializers.IntegerField()
    sort = serializers.ChoiceField(['asc', 'desc'])
    status = serializers.ChoiceField(choices=[
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled')
    ])
    
    class Meta:
        model = Order
        fields = ["buyer", "order", "status", "sort"]