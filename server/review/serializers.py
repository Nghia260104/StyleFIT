from rest_framework import serializers
from .models import Review
from account.models import Account
from product.models import Product
from order.models import Order

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        extra_kwargs = {
            'product': {'write_only': True},
            'seller': {'write_only': True}
        }
    
    def create(self, validated_data):
        review = Review.objects.create(**validated_data)
        return review
    
    def validate(self, data):
        if data['buyer'].role != 'BUYER':
            raise serializers.ValidationError("Only buyers can add reviews")
        if Order.objects.filter(buyer=data['buyer'], product=data['product']).exists() == False:
            raise serializers.ValidationError("Only buyers who have bought the product can add reviews")
        if data['rating'] < 0 or data['rating'] > 5:
            raise serializers.ValidationError("Rating must be between 0 and 5")
        if data['comment'] == '':
            raise serializers.ValidationError("Comment cannot be empty")
        if not Product.objects.filter(id=data['product']).exists():
            raise serializers.ValidationError("Product does not exist")
        return data