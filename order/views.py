from rest_framework import viewsets, mixins
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import CartItemSerializer, CartItemDetailSerializer
from .models import ShopCartItem, ShopCart


class ShopCartItemView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin, mixins.UpdateModelMixin, mixins.CreateModelMixin):
    permission_classes = [IsAuthenticated]

    # authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        cart, status = ShopCart.objects.get_or_create(owner=self.request.user)
        shop_cart = ShopCartItem.objects.select_related('cart_item').filter(cart_item=cart)
        return shop_cart

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'create':
            return CartItemSerializer
        else:
            return CartItemDetailSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
