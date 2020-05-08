from rest_framework import serializers
from .meal.models import Meal
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .profiles_api.models import UserProfile

class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing out APIView"""
    name = serializers.CharField(max_length=10)

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ('id', 'food_name', 'calorie', 'description', 'created_at', 'user_profile')
        extra_kwargs = {'user_profile': {'read_only':True}}

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'name', 'password', 'curr_calorie', 'max_calorie', 'is_limit' , 'meals')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            },
            'curr_calorie' : {
                'read_only': True
            },
            # 'max_calorie': {
            #     'write_only': True
            # },
            'is_limit' : {
                'read_only': True
            }

        }

    # def create(self, validated_data):
    #     user = UserProfile.objects.create_user(**validated_data)
    #     Token.objects.create(user=user)
    #     return user

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)  # as long as the fields are the same, we can just use this
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)