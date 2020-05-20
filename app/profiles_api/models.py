from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from rest_framework import status
from rest_framework.response import Response

from ..meal.models import Meal as m

from .serializer_user import MealSerializer1

from json import JSONEncoder

import json
import datetime

class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, name, password=None, max_calorie=2000):
        """Create a new user profile"""
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, max_calorie=max_calorie,)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password, max_calorie):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, name, password, max_calorie)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    curr_calorie = models.FloatField(default=0)
    max_calorie = models.FloatField(default=2000)

    is_limit = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve full name for user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    def __str__(self):
        """Return string representation of user"""
        return self.email

    def meals(self):
        #print(self.id)
        #print(self.email)
        meal = m.objects.filter(user_profile=self.id,created_at=datetime.datetime.now().strftime('%d%m%y'))
        #print(meal)
        serializer_class = MealSerializer1(meal, many=True)
        return serializer_class.data