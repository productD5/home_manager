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
    money = serializers.IntegerField(required=False , min_value=0)
    category = serializers.CharField(max_length=20)
    title = serializers.CharField(max_length=20)
    money_comment = serializers.CharField(max_length=100, required=False)

    def update(self, instance, validated_data):
            for attr, value in validated_data.items():
                if attr == 'money':
                    if value < 0:
                        raise serializers.ValidationError({'money': '金額は0以上でなければなりません。'})
                setattr(instance, attr, value)

            try: 
                instance.save()
            except Exception as e: 
                raise serializers.ValidationError({'error':f"Error updating instance: {str(e)}"})
    
            return instance