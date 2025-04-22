from . import views;
from django.urls import path;

urlpatterns = [
    path('signup/',views.RegisterView.as_view(),name='user-singup'), #新規登録処理
    path('login/',views.LoginView.as_view(),name='user-login'), #ログイン処理
    path('users/<str:user_id>/',views.UserDetailView.as_view(),name='user-detail'), #アカウント情報取得
    path('users/<str:user_id>/update',views.UserUpdateView.as_view(),name='user-update'), #アカウント情報更新
    path('delete/<str:user_id>/',views.CloseAccountView.as_view(), name='delete-user') #アカウント削除
]