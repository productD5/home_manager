from django.db import models

# Create your models here.
class home_money(models.Model):
    user_id = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    money_id = models.IntegerField(unique=True, primary_key=True, autoincrement=True)
    money = models.IntegerField(default=0)
    category = models.CharField(max_length=20)
    title = models.CharField(max_length=20)
    money_comment = models.CharField(max_length=100, blank=True)