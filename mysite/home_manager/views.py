from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import addMoneySerializer
from rest_framework.permissions import IsAuthenticated
# Create your views here.
class addMoneyView(APIView):
    """新規登録"""
    permission_classes = [IsAuthenticated] #認証が必要なAPIです

    def post(request, *args, **kwargs):
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