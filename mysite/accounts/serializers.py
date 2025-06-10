from rest_framework import serializers
from .models import User
#ユーザー登録シリアライザ
class  RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=30, write_only=True)
    password_confirmation = serializers.CharField(max_length=30, write_only=True)
    #userメタ情報
    class Meta:
        #シリアライザに渡すモデルを指定
        model = User
        fields = ('user_id','email','nickname','password','password_confirmation')
        extra_kwargs = {'password': {'write_only': True}} #パスワード非表示
        
    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError('パスワードが一致しません')
        return data
    
        #ユーザー作成関数
    def create(self, validated_data):
        validated_data.pop('password_confirmation')
        user = User.objects.create_user(**validated_data)
        return user
        
#ユーザーログインシリアライザ
class LoginSerializer(serializers.Serializer):
    #入力
    user_id = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=30, write_only=True)

    def validate(self,data):
        #DB内検索
        user_id = data.get('user_id')
        password = data.get('password')
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("user_idかパスワードが正しくありません!")

        if not user.check_password(password):
            #パスワードが一致しない場合
            raise serializers.ValidationError("user_idかパスワードが正しくありません")
        return data


#ユーザー情報更新シリアライザ
class UserUpdateSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=30, allow_blank=True)
    comment = serializers.CharField(max_length=100, allow_blank=True)
    

    def update(self, instance, validated_data):
        instance.nickname = validated_data.get('nickname',instance.nickname)
        instance.comment = validated_data.get('comment',instance.comment)
        instance.save()
        return instance  
    