from . import views;
from django.urls import path;

urlpatterns = [
    path('sighup/',views.RegisterView.as_view(),name='user-singup'), #新規登録処理
    path('login/',views.LoginView.as_view(),name='user-login') #ログイン処理
]