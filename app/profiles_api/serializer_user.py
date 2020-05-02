from rest_framework import serializers
from  ..meal.models import Meal

class MealSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ('id', 'food_name', 'calorie', 'description', 'created_at')
        #extra_kwargs = {'user_profile': {'read_only':True}}