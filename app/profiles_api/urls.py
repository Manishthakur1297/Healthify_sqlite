from ..profiles_api import views
from django.urls import path, include

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
#router.register('hello-viewset', views.HelloViewSet, basename='hello-viewset')
router.register('profile', views.UserProfileViewSet)
router.register('register', views.UserRegisterView)

urlpatterns = [
    #path('hello-view/', views.HelloApiView.as_view()),
    path('login/', views.UserLoginApiView.as_view()),
    #path('register/', views.UserRegisterView),
    path('', include(router.urls)),
]