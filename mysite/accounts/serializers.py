from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
#ユーザー登録シリアライザ
class  RegisterSerializer(serializers.ModelSerializer):
    #userメタ情報
    class Meta:
        #シリアライザに渡すモデルを指定
        model = User
        fields = ('user_id', 'password', 'nickname')
        extra_kwargs = {'password': {'write_only': True}} #パスワード非表示
        
    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError('パスワードが一致しません')
        return data
    
        #ユーザー作成関数
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
        
#ユーザーログインシリアライザ
class LoginSerializer(serializers.Serializer):
    #入力

    def validate(self,data):
        #DB内検索
        user_id = data.get('user_id')
        password = data.get('password')
        user = authenticate(user_id = user_id, password = password)
        #ユーザーが存在するか確認
        if user is not None:
            return data
        else:
            raise serializers.ValidationError('ログイン失敗')


#ユーザー情報更新シリアライザ
class UserUpdateSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=30, allow_blank=True)
    comment = serializers.CharField(max_length=100, allow_blank=True)

    def update(self, instance, validated_data):
        instance.nickname = validated_data.get('nickname',instance.nickname)
        instance.comment = validated_data.get('comment',instance.comment)
        instance.save()
        return instance  
    