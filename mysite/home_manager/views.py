from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import addMoneySerializer
from rest_framework.permissions import IsAuthenticated
from .models import home_money
# Create your views here.
class addMoneyView(APIView):
    """新規登録"""
    def post(self,request, *args, **kwargs):
        serializer = addMoneySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # エラーなし
            try:
                serializer.save(user_id=request.user) #DBに保存
            except Exception as e:
                # データベースエラー
                return Response({'error': 11,'message':f'Database error:{str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    class moneyDataView(APIView):
        """家計情報取得"""
        permission_classes = [IsAuthenticated]

        def get(self, request, *args, **kwargs):
            user_id = request.user
            try:
                # ユーザーの家計情報を取得
                money_data = user_id.homemoney_set.all()  # home_moneyモデルの関連名を使用
                if not money_data:
                    return Response({'error': 5, 'message': 'No money data found for this user'}, status=status.HTTP_404_NOT_FOUND)

                serializer = addMoneySerializer(money_data, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': 11, 'message': f'Database error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)