from rest_framework import serializers

from .models import ShopCart, ShopCartItem


class CartItemSerializer(serializers.ModelSerializer):
    product_url = serializers.HyperlinkedRelatedField(source='cart_product', view_name='product-detail', read_only=True)
    product_name = serializers.StringRelatedField(source='cart_product', read_only=True)
    owner = serializers.StringRelatedField(source='cart_item', read_only=True)

    class Meta:
        model = ShopCartItem
        fields = "__all__"
        read_only_fields = ['price', 'cart_item']

    def create(self, validated_data):
        request = self.context['request']
        product = self.validated_data.get('cart_product')
        number = self.validated_data.get('item_count')
        cart = ShopCart.objects.get(owner_id=request.user.id)
        return ShopCartItem.objects.create(
            cart_product_id=product.id, item_count=number, cart_item_id=cart.id)


class CartItemDetailSerializer(serializers.ModelSerializer):
    product_url = serializers.HyperlinkedRelatedField(view_name='product-detail', read_only=True, source='cart_product')
    product_name = serializers.StringRelatedField(source='cart_product')

    class Meta:
        model = ShopCartItem
        fields = '__all__'
        read_only_fields = ['price', 'cart_item', 'cart_product']

    def update(self, instance, validated_data):
        item_count = validated_data.get('item_count')
        if int(item_count) == 0:
            return instance.delete()
        return super().update(instance, validated_data)
