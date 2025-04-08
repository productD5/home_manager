from django.db import models
import hashlib
from datetime import timedelta
from django.utils import timezone

class User(models.Model):
    user_id = models.CharField(max_length=20, unique=True) #ユニークな値
    password = models.CharField(max_length=20)
    nickname = models.CharField(max_length=50)
    comment = models.CharField(max_length=100, blank=True ) #空白ok
    

def in_30_days():
    return timezone.now() + timedelta(days=30) #現在の時間から30日足したものを返す

class AccessToken(models.Model):
    #紐づけるユーザー
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    #アクセストークン(sha1でハッシュ化)
    token = models.CharField(max_length=40)

    #アクセス日時
    access_datetime = models.DateTimeField(default=in_30_days)

    def str(self):
        #メールアドレスとアクセス日時、トークンが見えるように設定
        dt = timezone.localtime(self.access_datetime).strftime('%Y/%m/%d %H:%M:%S')
        return self.user.user_id + '(' + dt + ') - ' + self.token
    
    @staticmethod
    def create(user: User):
        #既存のトークンを取得
        if AccessToken.objects.filter(user=user).exists(): #レコードがある場合はTrue
            #トークンが存在していた場合削除
            AccessToken.objects.get(user=user).delete()

        #トークンの作成(user_id、pasword、システムの日付のハッシュ値とする)
        dt = timezone.now()
        str = user.user_id + user.password + dt.strftime('%Y%m%d%H%M%S%f')
        hash = hashlib.sha1(str.encode('utf-8')).hexdigest()

        #DBに追加情報を記録
        token = AccessToken.objects.create(
            user=user,
            token=hash,
            access_datetime=dt
        )
        return token