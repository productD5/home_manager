from django.contrib import admin
from django.urls import path,include
urlpatterns = [
    path('admin/', admin.site.urls), #管理画面
    path('accounts/',include('accounts.paths')), #アカウント画面
    path('home_manager/',include('home_manager.paths')), #アプリ画面
    
]
