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
        fields = ['name', 'description', 'percentage', 'season', 'product', 'category', 'limit', 'used_number']

    def validate(self, data):
        if 'limit' in data:
            if data['limit'] is None or data['limit'] <= 0:
                raise serializers.ValidationError({"limit": "Limit must be greater than 0"})
            
            # Check if new limit would be less than current used_number
            instance = self.instance
            if data['limit'] < instance.used_number:
                raise serializers.ValidationError(
                    {"limit": "New limit cannot be less than current used number"}
                )

        

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
        # Remove None values from validated_data to prevent overwriting with None
        validated_data = {k: v for k, v in validated_data.items() if v is not None}
        
        # Remove empty strings for required fields
        if 'description' in validated_data and validated_data['description'] == '':
            validated_data.pop('description')
        if 'season' in validated_data and validated_data['season'] == '':
            validated_data.pop('season')
            
        # Update only the fields that are present in validated_data
        for field, value in validated_data.items():
            setattr(instance, field, value)
            
        instance.save()
        return instance