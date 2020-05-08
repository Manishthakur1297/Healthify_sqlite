from ..profiles_api import views
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

router = DefaultRouter()
#router.register('hello-viewset', views.HelloViewSet, basename='hello-viewset')
router.register('users', views.UserProfileViewSet)
router.register('register', views.UserRegisterView)

urlpatterns = [
    #path('hello-view/', views.HelloApiView.as_view()),
    #path('login/', views.UserLoginApiView.as_view()),
    #path('register/', views.UserRegisterView),
    path('', include(router.urls)),
    path('login/', views.ObtainTokenPairWithEmailView.as_view(), name='login_token'),  # override sjwt stock token
    path('login/refresh/', jwt_views.TokenRefreshView.as_view(), name='login_refresh'),
]