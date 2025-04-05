from django.contrib import admin
from django.urls import path,include
urlpatterns = [
    path('admin/', admin.site.urls), #管理画面
    path('accounts/',include('accounts.urls')), #アカウント画面
]
