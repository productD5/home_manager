from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import addMoneySerializer, moneyDataViewSerializer
from rest_framework.permissions import IsAuthenticated
from .models import home_money
from accounts.models import User
from rest_framework.authtoken.models import Token
from datetime import timedelta
from django.utils import timezone

"""新規登録"""
class addMoneyView(APIView):


    def post(self,request, *args, **kwargs):
        serializer = addMoneySerializer(data=request.data)
        
        # ユーザーIDを取得
        user_id = request.data.get('user_id')
        
        try:
            user = User.objects.get(user_id=user_id)  # user_idでユーザーを取得
        except User.DoesNotExist:
            print("Not User found")
            return Response({"message": "Not User found"}, status=404)
        
        if serializer.is_valid(raise_exception=True):
            # エラーなし
            try:
                
                serializer.save() #DBに保存
                print("データを保存しました")
            except Exception as e:
                # データベースエラー
                return Response({'error': 11,'message':f'Database error:{str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
"""家計情報取得"""
class moneyDataView(APIView):


    def get(self, request, user_id,*args, **kwargs):
        TOKEN_LIFETIME_MINUTES = 100  # トークンの有効期限（分）

        #ユーザー情報の取得
        try:
            user = User.objects.get(user_id = user_id) #user_idでユーザーを取得

        except User.DoesNotExist:
            return Response({"message":"Not User found"},status=404)
        
        #トークン状態を確認
        try:
            token = Token.objects.get(user=user) #userに紐づくトークンを取得

            if (token.created + timedelta(minutes = TOKEN_LIFETIME_MINUTES)) < timezone.now() :
            # トークンが期限切れの場合
                token.delete()
                return Response({"message": "Token is expired"}, status=401)
            
            # ユーザーの家計情報を取得
            money_data = home_money.objects.filter(user_id__user_id=user_id)
            
            if not money_data:
                return Response(status=status.HTTP_200_OK)

            serializer = moneyDataViewSerializer(money_data, many=True)
            print("データを取得しました")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 11, 'message': f'Database error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

"""家計情報更新"""
class updateMoneyView(APIView):

    def put(self, request, money_id, *args, **kwargs):
        try:
            money_instance = home_money.objects.get(money_id=money_id)
        except home_money.DoesNotExist:
            return Response({"message": "Money record not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = addMoneySerializer(money_instance, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            try:
                serializer.save()  # DBに保存
            except Exception as e:
                return Response({'error': 11, 'message': f'Database error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            print("データを更新しました")
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
"""家計情報削除"""
class deleteMoneyView(APIView):
    def delete(self, request, money_id, *args, **kwargs):
        try:
            money_instance = home_money.objects.get(money_id=money_id)
        except home_money.DoesNotExist:
            return Response({"message": "Money record not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            money_instance.delete()
            print("データを削除しました")
            return Response({"message": "Money record deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': 11, 'message': f'Database error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)