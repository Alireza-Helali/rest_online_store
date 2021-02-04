from django.conf import settings
from django.db import models
from product.models import Product
import uuid


class ShopCart(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    payment_date = models.DateField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)

    @property
    def cart_length(self):
        return self.cart_item.count()

    @property
    def factor_num(self):
        return str(uuid.uuid4()[:13])

    @property
    def sum_cart(self):
        items = self.cart_item.all()
        item_sum = 0
        for item in items:
            item_sum += item.price
        return item_sum


class ShopCartItem(models.Model):
    item_count = models.PositiveIntegerField(default=1)
    cart_item = models.ForeignKey(ShopCart, on_delete=models.CASCADE, related_name='cart_item')
    cart_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_product')
    price = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['cart_item', 'cart_product'], name='cart item constraint')
        ]

    def save(self, *args, **kwargs):
        product_price = self.cart_product.price
        self.price = product_price * self.item_count
        return super(ShopCartItem, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.cart_product.id} - {self.cart_product.name}"
