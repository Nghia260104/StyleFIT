from rest_framework import serializers
from .models import Review
from account.models import Account
from product.models import Product
from order.models import Order
from orderdetail.models import OrderDetail

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
        try:
            account = Account.objects.get(username=data['buyer'])
        except Account.DoesNotExist:
            raise serializers.ValidationError("Buyer does not exist")
        
        if account.role != 'CUSTOMER':
            raise serializers.ValidationError("Only buyers can add reviews")
        
        # Ensure 'product' is passed as an ID, not an instance
        product_id = data['product'].id if isinstance(data['product'], Product) else data['product']
        if not Product.objects.filter(id=product_id).exists():
            raise serializers.ValidationError("Product does not exist")
        
        if data['rating'] < 0 or data['rating'] > 5:
            raise serializers.ValidationError("Rating must be between 0 and 5")
        
        if data['content'] == '':
            raise serializers.ValidationError("Comment cannot be empty")
        
        orderdetails = OrderDetail.objects.filter(
            order__buyer=data['buyer'], 
            product_id=product_id
        )
        if not orderdetails.exists():
            raise serializers.ValidationError("Only buyers who have purchased the product can add reviews")
        
        length = len(orderdetails)
        for orderdetail in orderdetails:
            if orderdetail.order.status == 'DELIVERED':
                length -= 1
        if length == len(orderdetails):
            raise serializers.ValidationError("Only buyers who have received the product can add reviews")

        return data
