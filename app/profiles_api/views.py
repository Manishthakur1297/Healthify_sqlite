from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework.response import Response
from ..profiles_api.models import UserProfile
from ..profiles_api import permissions

from rest_framework.authentication import TokenAuthentication
from ..serializers import UserProfileSerializer

from rest_framework import viewsets

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


def home(request):
    return render(request,'index.html')

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile, IsAuthenticated, )

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)

    # def create(self, request):
    #     if request.method == 'POST':
    #         serializer = UserProfileSerializer(data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = {'message': 'User Not Found'}
        return Response(response, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        if request.user.is_superuser:
            user = UserProfile.objects.all()
            serializer_class = UserProfileSerializer(user, many=True)
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        else:
            user = UserProfile.objects.get(id=request.user.id)
            serializer_class = UserProfileSerializer(user, many=False)
            return Response(serializer_class.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        try:
            user = UserProfile.objects.get(id=kwargs['pk'])
            if user.id==request.user.id or request.user.is_superuser:
                serializer_class = UserProfileSerializer(user, many=False)
                return Response(serializer_class.data, status=status.HTTP_200_OK)
            else:
                response = {'message': 'Not Authorised to view or edit user'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except:
            response = {'message': 'User Not Found'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)


class UserLoginApiView(ObtainAuthToken):
   """Handle creating user authentication tokens"""
   renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserRegisterView(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    def retrieve(self, request, *args, **kwargs):
        response = {'message': 'User Not Found'}
        return Response(response, status=status.HTTP_404_NOT_FOUND)

    def list(self, request, *args, **kwargs):
        response = {'message': 'User Not Found'}
        return Response(response, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        response = {'message': 'User Not Found'}
        return Response(response, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, *args, **kwargs):
        response = {'message': 'User Not Found'}
        return Response(response, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        response = {'message': 'User Not Found'}
        return Response(response, status=status.HTTP_404_NOT_FOUND)