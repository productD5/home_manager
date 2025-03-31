from rest_framework import serializers
from .models import User

class  RegisterSerializer(serializers.ModelSerializer):
    #userメタ情報
    class Meta:
        model = User
        fields = ('user_id', 'password', 'nickname')
        extra_kwargs = {'password': {'write_only': True}}

        #ユーザー作成関数
        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            return user