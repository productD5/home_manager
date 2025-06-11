from django.db import models
from accounts.models import User
# Create your models here.

class home_money(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    money_id = models.AutoField(unique=True, primary_key=True,)
    money = models.IntegerField(default=0)
    category = models.CharField(max_length=20)
    title = models.CharField(max_length=20)
    money_comment = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user_id} - {self.money_id} - {self.category} - {self.title} - {self.money}"