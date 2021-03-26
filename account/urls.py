from django.urls import path, include
from .api import UserView, ProfileView, RegisterView

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register('user', UserView, basename='user')
router.register('profile', ProfileView, basename='profile')

urlpatterns = [
    # path('token', TokenApiView.as_view(), name='token'),
    path('auth/', include('rest_framework.urls'), name='auth'),
    path('register', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls))
]
