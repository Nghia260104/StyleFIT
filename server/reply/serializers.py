from rest_framework import serializers
from .models import Reply
from review.models import Review
from account.models import Account

class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = '__all__'
        extra_kwargs = {
            'review': {'write_only': True},
            'seller': {'write_only': True}
        }
    
    def create(self, validated_data):
        reply = Reply.objects.create(**validated_data)
        return reply
    
    def validate(self, data):
        if data['seller'].role != 'SELLER':
            raise serializers.ValidationError("Only sellers can add replies")
        if not Review.objects.filter(id=data['review']).exists():
            raise serializers.ValidationError("Review does not exist")
        return data