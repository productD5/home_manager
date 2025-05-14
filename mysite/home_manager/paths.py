from . import views;
from django.urls import path;

urlpatterns = [
    path('register/', views.HomeRegisterView.as_view(), name='home-register'), #家計情報登録
]