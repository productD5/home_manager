from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED,HTTP_200_OK,HTTP_401_UNAUTHORIZED
from .serializers import RegisterSerializer,LoginSerializer,UserUpdateSerializer, UserDetailSerializer
from .models import User
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from datetime import timedelta
from django.utils import timezone


"""新規登録"""
class RegisterView(APIView):
    
    authentication_classes = []
    @staticmethod
    def post(request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data) #シリアライザをインスタンス化
        if serializer.is_valid(raise_exception=True):

            # UserIDがすでに使われていた場合
            if User.objects.filter(user_id=serializer.validated_data['user_id']).exists():
                return Response({'error': 3}, status=HTTP_400_BAD_REQUEST)

            # エラーなし
            try:
                serializer.save() #DBに保存
            except Exception as e:
                # データベースエラー
                return Response({'error': 11,'message':f'Database error:{str(e)}'}, status=HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
"""ログイン"""
class LoginView(GenericAPIView):
    
    authentication_classes = []

    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)

        if serializer.is_valid(raise_exception=True):
            user_id = serializer.validated_data['user_id']
            password = serializer.validated_data['password']

            #ユーザー認証
            user = authenticate(request, username = user_id, password = password)

            if user is None:
                return Response({'error':2, 'message': '認証失敗'})
            token, created = Token.objects.get_or_create(user=user)  # トークンを取得または作成
            if not created:
                # トークンが既に存在する場合は、トークンを更新
                token.delete()
                token = Token.objects.create(user=user)

            #ログイン成功
            return Response({
                'detail': 'ログイン成功',
                'error': 0,
                'message': 'ログインに成功しました',
                'token': token.key,
                'nickname': user.nickname,
                'user_id':user.user_id,
            },status=HTTP_200_OK)
        
        return Response( serializer.errors, status=HTTP_400_BAD_REQUEST )
    
"""ユーザー情報取得"""
class UserDetailView(APIView):
    

    def get(self,request, user_id):
        TOKEN_LIFETIME_MINUTES = 5  # トークンの有効期限（分）

        #ユーザー情報の取得
        try:
            user = User.objects.get(user_id = user_id) #user_idでユーザーを取得
            print(user)

        except User.DoesNotExist:
            return Response({"message":"Not User found"},status=404)
        
        #トークン状態を確認
        try:
            token = Token.objects.get(user=user) #userに紐づくトークンを取得

        except Token.DoesNotExist:
            # トークンが存在しない場合
            return Response({"message": "Token does not exist"}, status=HTTP_401_UNAUTHORIZED)
        
        if (token.created + timedelta(minutes = TOKEN_LIFETIME_MINUTES)) < timezone.now() :
            # トークンが期限切れの場合
            token.delete()
            return Response({"message": "Token is expired"}, status=HTTP_401_UNAUTHORIZED)
        
        serializer = UserDetailSerializer(user)  # シリアライザーを使用
        response_data = {
            "message": "User details by user_id",
            "user": serializer.data
        }
        return Response(response_data, status=HTTP_200_OK)


"""ユーザー情報更新"""
class UserUpdateView(APIView):

    def patch(self ,request, user_id):
        #ユーザー情報取得
        try:
            user = User.objects.get(user_id = user_id)

        except User.DoesNotExist:
            #ユーザーが存在しない場合
            return Response({"message": "No User found"}, status=404)
        
        try:
            token = Token.objects.get(user=user)  # userに紐づくトークンを取得
        except Token.DoesNotExist:
            # トークンが存在しない場合
            return Response({"message": "Token does not exist"}, status=HTTP_401_UNAUTHORIZED)
        
        #トークンの有効期限チェック
        TOKEN_LIFETIME_MINUTES = 100  # トークンの有効期限（分）
        
        if (token.created + timedelta(minutes=TOKEN_LIFETIME_MINUTES)) < timezone.now():
            # トークンが期限切れの場合
            token.delete()
            return Response({"message": "Token is expired"}, status=HTTP_401_UNAUTHORIZED)
            
        
        serialazer =  UserUpdateSerializer(user, data=request.data, partial=True)
        #データが正しいかの検証(値が正しいか等)
        if serialazer.is_valid():
            #形式の保存
            serialazer.save()

            respose_data = {
                "message" : "User successFully updated",
                "user": {
                    "nickname": user.nickname,
                    "comment" : user.comment
                }
            }
            return Response(respose_data, status=200)
        
        else: 
            #エラーメッセージの表示
            error_message = serialazer.errors.get('non_field_error',['User updation failed'])[0]
            return Response({"message": "User updated failed","cause": error_message}, status=400)
        
    #ポストが許可されていなかった場合
    def post(self ,request, user_id):
        return Response({"message": "Methop not allowed"}, status=400)
    
"""アカウント削除"""
class CloseAccountView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request, user_id):
        #アカウント削除処理
        user = User.objects.filter(user_id=user_id).first()
        if not user:
            #ユーザーが存在しない場合
            return Response({"message": "No User found"}, status=404)
        user.delete()
            
        return Response({"message": "Account and user successfully removed"}, status=200)