from rest_framework import serializers
from .models import home_money

"""新規登録用シリアライザ"""
class addMoneySerializer(serializers.ModelSerializer):
    class Meta:
        model = home_money
        fields = ('user_id', 'money', 'category', 'title', 'money_comment')
        extra_kwargs = {
            'user_id': {'required': True},
            'money': {'required': True},
            'category': {'required': True},
            'title': {'required': True},
            'money_comment': {'required': False}
        }
    def create(self, validated_data):
        return home_money.objects.create(**validated_data)

"""家計情報取得用シリアライザ"""
class moneyDataViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = home_money
        fields = ('money_id','money', 'category', 'title', 'money_comment')
        extra_kwargs = {
            'money_id': {'required': True},
            'money': {'required': True},
            'category': {'required': True},
            'title': {'required': True},
            'money_comment': {'required': False}
        }

"""家計簿更新シリアライザ"""
class updateMoneySerializer(serializers.ModelSerializer):
    class Meta:
        model = home_money
        fields = ('money', 'category', 'title', 'money_comment')
        extra_kwargs = {
            'money': {'required': True},
            'category': {'required': True},
            'title': {'required': True},
            'money_comment': {'required': False}
        }
    
    def update(self, instance, validated_data):
        instance.money = validated_data.get('money', instance.money)
        instance.category = validated_data.get('category', instance.category)
        instance.title = validated_data.get('title', instance.title)
        instance.money_comment = validated_data.get('money_comment', instance.money_comment)
        instance.save()
        return instance
    

    