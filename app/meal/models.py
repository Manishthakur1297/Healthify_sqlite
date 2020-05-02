from django.db import models

from django.conf import settings

class Meal(models.Model):
    food_name = models.CharField(max_length=32)
    calorie = models.DecimalField(decimal_places=2,max_digits=20,default=0)
    description = models.TextField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    #limit = models.BooleanField(default=False)
    user_profile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.food_name
