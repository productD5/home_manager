from rest_framework import serializers
from .models import User

class  RegisterSerializer(serializers.ModelSerializer):
    #userメタ情報
    class Meta:
        model = User
        fields = ('user_id', 'password', 'nickname')
        extra_kwargs = {'password': {'write_only': True}} #パスワード非表示

        #ユーザー作成関数
        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            return user
    
class LoginSerializer(serializers.Serializer):
    #入力
    user_id = serializers.CharField(max_length=255,write_only=True)
    password = serializers.CharField(write_only=True,style={'input_type':'password'})

    def validate(self,data):
        #DB内検索
        user_id = data.get('user_id')
        password = data.get('password')
        userid = User.objects.get(user_id = user_id)
        re_password = User.objects.get(password = password)

        #検証
        if user_id == userid.user_id:
            if password == re_password.password:
                return data
            
            else:
                raise serializers.ValidationError('ログイン失敗')
            
class UserUpdateSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=30, allow_blank=True)
    comment = serializers.CharField(max_length=100, allow_blank=True)

    def update(self, instance, validated_data):
        instance.nickname = validated_data.get('nickname',instance.nickname)
        instance.comment = validated_data.get('comment',instance.comment)
        instance.save()
        return instance
    