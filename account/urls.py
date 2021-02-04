from django.urls import path, include
from .api import TokenApiView, UserView, ProfileView

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('user', UserView, basename='user')
router.register('profile', ProfileView, basename='profile')

urlpatterns = [
    path('token', TokenApiView.as_view(), name='token'),
    # path('profile/<int:pk>', ProfileView.as_view(), name='profile-detail'),
    path('', include(router.urls))
]
