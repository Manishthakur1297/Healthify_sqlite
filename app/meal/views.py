from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import Meal
from ..serializers import MealSerializer#, UserSerializer
from .utils import nutritionnix_calorie_api
from django.http.request import QueryDict, MultiValueDict
from ..profiles_api import permissions

from ..profiles_api.models import UserProfile

class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    #authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated,)
    #http_method_names = ['get' , 'post', 'delete']

    # def perform_create(self, serializer):
    #     """Sets the user profile to the logged in user"""
    #     serializer.save(user_profile=self.request.user)

    def list(self, request):
        if request.user.is_superuser:
            meal = Meal.objects.all()
            serializer_class = MealSerializer(meal, many=True)
        else:
            print(request.data)
            print(request.user.id)
            meal = Meal.objects.filter(user_profile=request.user.id)
            print(meal)
            serializer_class = MealSerializer(meal, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        try:
            meal = Meal.objects.get(id=kwargs['pk'])
            if meal.user_profile.id==request.user.id or request.user.is_superuser:
                serializer_class = MealSerializer(meal, many=False)
                return Response(serializer_class.data, status=status.HTTP_200_OK)
            else:
                response = {'message': 'Not Authorised to view or edit meal'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except:
            response = {'message': 'Meal Not Found'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)


    def create(self, request):
        if request.method=='POST':
            data = dict(request.data)
            if len(data['calorie'][0])==0 or float(data['calorie'][0])==float(0):
                flag,val = nutritionnix_calorie_api(data['food_name'][0])
                if flag:
                    data['calorie'][0] = val
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

            query_dict = QueryDict('', mutable=True)
            query_dict.update(MultiValueDict(data))
            serializer = MealSerializer(data = query_dict)
            if serializer.is_valid():
                try:
                    user = UserProfile.objects.get(pk=self.request.user.id)
                    user.curr_calorie+=float(data['calorie'][0])
                    if user.curr_calorie < user.max_calorie:
                        user.is_limit = False
                    else:
                        user.is_limit = True
                    user.save()
                except:
                    return Response(status=status.HTTP_404_NOT_FOUND)
                serializer.save(user_profile=self.request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            snippet = Meal.objects.get(pk=pk)
        except Meal.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'PUT':
            calorie = 0
            if snippet.food_name==request.data['food_name'] and float(request.data['calorie'])!=float(0):
                calorie = request.data['calorie']
                serializer = MealSerializer(snippet, data=request.data)
            else:
                data = dict(request.data)
                if not data['calorie'] or float(data['calorie'][0]) == float(0) \
                        or float(snippet.calorie)==float(data['calorie'][0]):
                    flag, val = nutritionnix_calorie_api(data['food_name'][0])
                    if flag:
                        data['calorie'][0] = val
                    else:
                        return Response(status=status.HTTP_400_BAD_REQUEST)
                calorie = data['calorie'][0]
                query_dict = QueryDict('', mutable=True)
                query_dict.update(MultiValueDict(data))
                serializer = MealSerializer(snippet, data=query_dict)


            if serializer.is_valid():
                try:
                    if request.user.is_superuser:
                        user = UserProfile.objects.get(pk=snippet.user_profile.id)
                    else:
                        user = UserProfile.objects.get(pk=self.request.user.id)

                    user.curr_calorie -= float(snippet.calorie)
                    user.curr_calorie += float(calorie)
                    if user.curr_calorie < user.max_calorie:
                        user.is_limit = False
                    else:
                        user.is_limit = True
                    user.save()
                except:
                    return Response(status=status.HTTP_404_NOT_FOUND)
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        calorie = instance.calorie
        try:
            if request.user.is_superuser:
                user = UserProfile.objects.get(pk=instance.user_profile.id)
            else:
                user = UserProfile.objects.get(pk=self.request.user.id)
            user.curr_calorie -= float(calorie)
            if user.curr_calorie < user.max_calorie:
                user.is_limit = False
            else:
                user.is_limit = True
            user.save()
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


    # def partial_update(self, request, *args, **kwargs):
    #     print(args)
    #     print(kwargs)
    #     print(request.data)
    #     super(MealViewSet, self).partial_update(request,args,kwargs)

    # def partial_update(self, request, pk=None):
    #     serialized = MealSerializer(request.user, data=request.data, partial=True)
    #     return Response(status=status.HTTP_202_ACCEPTED)


