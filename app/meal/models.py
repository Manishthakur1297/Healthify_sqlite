from django.db import models

from django.conf import settings
import datetime

class Meal(models.Model):
    food_name = models.CharField(max_length=32)
    calorie = models.FloatField(default=0)
    description = models.TextField(default="", max_length=256)
    #created_at = models.DateTimeField(auto_now_add=True)
    #x = datetime.datetime.now()
    created_at = models.TextField(default=datetime.datetime.now().strftime('%d%m%y'))
    #limit = models.BooleanField(default=False)
    user_profile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.food_name
