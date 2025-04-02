from django.db import models

# Create your models here.

class User(models.Model):
    user_id = models.CharField(max_length=20, unique=True) #ユニークな値
    password = models.CharField(max_length=20)
    nickname = models.CharField(max_length=50)
    comment = models.CharField(max_length=100, blank=True ) #空白ok

    def __str__(self):
        return self.user_id