from .views import ShopCartItemView

from django.urls import path, include

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('order', ShopCartItemView, basename='order')

urlpatterns = [
    path('', include(router.urls))
]
