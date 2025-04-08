from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED
from .serializers import RegisterSerializer,LoginSerializer
from .models import User,AccessToken
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny 
from rest_framework.generics import GenericAPIView


class RegisterView(APIView):
    """新規登録API"""
    @staticmethod
    def post(request, *args, **kwargs):
        print(request.data)
        serializer = RegisterSerializer(data=request.data) #シリアライザをインスタンス化インスタンス化

        if serializer.is_valid(raise_exception=True):
            # パスワードと確認パスワードが一致しない場合
            if serializer.validated_data['password'] != request.data['password_confirmation']:
                return Response({'error': 2}, status=HTTP_400_BAD_REQUEST)

            # UserIDがすでに使われていた場合
            if User.objects.filter(user_id=serializer.validated_data['user_id']).exists():
                return Response({'error': 3}, status=HTTP_400_BAD_REQUEST)

            # エラーなし
            try:
                serializer.save() #DBに保存
            except:
                # データベースエラー
                return Response({'error': 11}, status=HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
class LoginView(GenericAPIView):
    """ログインApi"""
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        #クライアントエラーチェック
        if serializer.is_valid(raise_exception = True):
            #UserオブジェクトをDBから取得
            user = User.objects.get(user_id = serializer.validated_data['user_id'])
            user_id = serializer.validated_data['user_id']

            #トークンを生成
            token = AccessToken.create(user)
            return Response({'detail':"ログインが成功しました",'error':0, 'token':token.token, 'user_id': user_id})
        return Response({'error':1},status=HTTP_400_BAD_REQUEST)
    

class UserDetailView(APIView):
    def get(self,reqest, user_id):
        #ユーザー情報の取得
        user = User.objects.filter(user_id = user_id).first #一件目を取得
        if not user:
            #userが存在しない場合
            return Response({"messerge":"Not User found"},stats=404)
        
        response_date ={
            "message": "User details by user_id",
            "user":{
                "user_id": User.user_id,
                "nickname": User.nickname,
                "comment" :User.comment
            }
        }

        return Response(response_date,status=200)
