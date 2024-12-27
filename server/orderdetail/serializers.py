from rest_framework import serializers
from .models import OrderDetail
from product.models import Product
from order.models import Order

class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = '__all__'
        extra_kwargs = {
            'order': {'write_only': True},
            'product': {'write_only': True}
        }

    # buyer = serializers.CharField()  # Include buyer field
    # product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    # quantity = serializers.IntegerField()

    # Use only product and quantity for the OrderDetail model
    # def create(self, validated_data):
    #     validated_data.pop('buyer', None)  # Remove buyer before saving
    #     return OrderDetail.objects.create(**validated_data)