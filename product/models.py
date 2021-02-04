from django.db import models
from account.models import Supplier


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to=f'static/images')
    quantity = models.PositiveIntegerField(default=0)
    subcategory = models.ForeignKey('SubCategory', on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"{self.pk}/{self.name.replace(' ', '-')}"


class Gallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='static/images', null=True, blank=True)

    def __str__(self):
        return self.product.name


class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class SubCategory(models.Model):
    title = models.CharField(max_length=20, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategory')

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=15)
    product = models.ManyToManyField(Product)

    def __str__(self):
        return self.title

