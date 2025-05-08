from rest_framework import serializers
from .models import home_money

#家計簿登録
class HomeMoneyRegistrSerializer(serializers.ModelSerializer):
    class Meta:
        model = home_money
        fields = ['user_id', 'money_id', 'money', 'category', 'title', 'money_comment']
        extra_kwargs = {
            'user_id': {'read_only': True},
            'money_id': {'read_only': True}
        }
    def create(self, validated_data):
        return home_money.objects.create(**validated_data)


#家計簿更新
class HomeMoneyUpdateSerializer(serializers.ModelSerializer):
    money = serializers.IntegerField(required=False)
    category = serializers.CharField(max_length=20)
    title = serializers.CharField(max_length=20)
    money_comment = serializers.CharField(max_length=100, required=False)

    def update(self, instance, validated_data):
        instance.money = validated_data.get('money', instance.money)
        instance.category = validated_data.get('category', instance.category)
        instance.title = validated_data.get('title', instance.title)
        instance.money_comment = validated_data.get('money_comment', instance.money_comment)
        instance.save()
        return instance