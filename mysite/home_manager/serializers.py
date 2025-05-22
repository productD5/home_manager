from rest_framework import serializers
from .models import home_money

class addMoneySerializer(serializers.ModelSerializer):
    class Meta:
        model = home_money
        fields = ('user_id', 'money_id', 'money', 'category', 'title', 'money_comment')
        extra_kwargs = {
            'user_id': {'required': True},
            'money_id': {'required': True},
            'money': {'required': True},
            'category': {'required': True},
            'title': {'required': True},
            'money_comment': {'required': False}
        }
    def create(self, validated_data):
        return home_money.objects.create(**validated_data)
    