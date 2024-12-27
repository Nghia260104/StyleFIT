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
        # Edit this line to make sure data['limit'] > 0 
        if data['limit'] <= 0:
            raise serializers.ValidationError("Limit must be greater than 0") 
        seller = data['seller']
        season = data['season']
        year = data['year']
        account_role = Account.objects.get(username=seller).role
        if account_role != 'SELLER':
            raise serializers.ValidationError("Only sellers can create discounts")
        if Discount.objects.filter(seller=seller, season=season, year=year).exists():
            raise serializers.ValidationError("Discount already exists")
        
        return data
    
class DiscountEditSerializer(serializers.ModelSerializer):
    seller_id = serializers.IntegerField(write_only=True,required=True)
    name = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=False)  # Don't allow blank for required fields
    percentage = serializers.IntegerField(required=False, allow_null=False)  # Don't allow null for required fields
    season = serializers.CharField(required=False, allow_blank=False)  # Don't allow blank for required fields
    product = serializers.ListField(child=serializers.IntegerField(), required=False, allow_empty=True)
    category = serializers.ListField(child=serializers.CharField(), required=False, allow_empty=True)
    limit = serializers.IntegerField(required=False, allow_null=False)  # Don't allow null for required fields
    used_number = serializers.IntegerField(required=False, allow_null=False)  # Don't allow null for required fields
    
    class Meta:
        model = Discount
        fields = ['seller_id', 'name', 'description', 'percentage', 'season', 'product', 'category', 'limit', 'used_number']

    def validate(self, data):
        try:
            seller = Account.objects.get(id=data['seller_id'])
        except Account.DoesNotExist:
            raise serializers.ValidationError({"seller_id": "Seller not found"})
        
        if seller.role != 'SELLER':
            raise serializers.ValidationError({"seller_id": "Only sellers can edit discounts"})

        if 'limit' in data:
            if data['limit'] is None or data['limit'] <= 0:
                raise serializers.ValidationError({"limit": "Limit must be greater than 0"})
            
            # Check if new limit would be less than current used_number
            instance = self.instance
            if data['limit'] < instance.used_number:
                raise serializers.ValidationError(
                    {"limit": "New limit cannot be less than current used number"}
                )

        if 'used_number' in data:
            # Check if new used_number would be greater than limit
            instance = self.instance
            limit = data.get('limit', instance.limit)
            if data['used_number'] > limit:
                raise serializers.ValidationError(
                    {"used_number": "Used number cannot exceed limit"}
                )

            # Check if used_number equals limit
            if data['used_number'] == limit:
                # We 'll handle deletion in the view
                data['should_delete'] = True

        # Check if season is being updated and if a discount already exists for that season
        if 'season' in data and data['season'] != instance.season:
            if Discount.objects.filter(
                seller=instance.seller,
                season=data['season'],
                year=instance.year
            ).exists():
                raise serializers.ValidationError({"season": "Discount already exists for this season and year"})
        
        return data

    def update(self, instance, validated_data):
        validated_data.pop('seller_id')  # Remove seller_id from validated_data

        validated_data = {k: v for k, v in validated_data.items() if v is not None}
        
        if 'description' in validated_data and validated_data['description'] == '':
            validated_data.pop('description')
        if 'season' in validated_data and validated_data['season'] == '':
            validated_data.pop('season')
            
        # Update only the fields that are present in validated_data
        for field, value in validated_data.items():
            setattr(instance, field, value)
            
        instance.save()
        return instance