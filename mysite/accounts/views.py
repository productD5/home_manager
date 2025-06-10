from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED
from .serializers import RegisterSerializer,LoginSerializer,UserUpdateSerializer
from .models import User
from rest_framework.permissions import AllowAny 
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class RegisterView(APIView):
    """新規登録"""
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
    
class LoginView(GenericAPIView):
    """ログイン"""
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
            # クライアントエラーチェック
        if serializer.is_valid(raise_exception=True):
            try:
                # UserオブジェクトをDBから取得
                user = User.objects.get(user_id=serializer.validated_data['user_id'])
            except ObjectDoesNotExist:
                return Response({'error': 2, 'message': 'User not found'}, status=HTTP_400_BAD_REQUEST)

            try:
                # トークンを生成
                token, created =Token.objects.get_or_create(user=user)
                if created:
                    token.save()
            except Exception as e:
                print(f"Token generation error: {str(e)}")
                return Response({'error': 4, 'message': f'Token generation failed: {str(e)}'}, status=HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'detail': "ログインが成功しました", 'error': 0, 'token': token.key, 'user_id': user.user_id})
        return Response({'error': 3, 'message': 'Invalid credentials'}, status=HTTP_400_BAD_REQUEST)
    

class UserDetailView(APIView):
    """ユーザー情報取得"""
    def get(self,request, user_id):
        #ユーザー情報の取得
        user = User.objects.filter(user_id = user_id).first() #一件目を取得(ここで属性の評価を行う))
        if not user:
            #userが存在しない場合
            return Response({"messerge":"Not User found"},status=404)
        else:
            response_date ={
                "message": "User details by user_id",
                "user":{
                "user_id": user.user_id,
                "nickname": user.nickname,
                "comment" :user.comment
                }
            }
            return Response(response_date,status=200)



class UserUpdateView(APIView):
    """ユーザー情報更新"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def patch(self ,request, user_id):
        #ユーザー情報取得
        user= User.objects.filter(user_id = user_id).first()

        if not user:
            #ユーザーが存在しない場合
            return Response({"message": "No User found"}, status=404)
        
        if request.user.user_id != user_id:
            #異なるIDだった場合
            return Response({"message": "No permission for Update"}, status=403)
        
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
    

class CloseAccountView(APIView):
    """アカウント削除"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, user_id):
        #アカウント削除処理
        user = User.objects.filter(user_id=user_id).first()
        if not user:
            #ユーザーが存在しない場合
            return Response({"message": "No User found"}, status=404)
        user.delete()
            
        return Response({"message": "Account and user successfully removed"}, status=200)
