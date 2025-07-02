from . import views;
from django.urls import path;

urlpatterns = [
    path('register/', views.addMoneyView.as_view(), name='home-register'), #家計情報登録
    path('view/<str:user_id>', views.moneyDataView.as_view(), name='home-view'), #家計情報取得
    path('editMoney/<int:money_id>', views.updateMoneyView.as_view(), name='home-update'), #家計情報更新
    path('deleteMoney/<int:money_id>', views.deleteMoneyView.as_view(), name='home-delete'), #家計情報削除
]