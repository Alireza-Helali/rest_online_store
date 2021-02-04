from rest_framework import serializers

from .models import Product, Supplier, Category, SubCategory


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    subcategory = serializers.HyperlinkedRelatedField(queryset=Product.objects.select_related('subcategory_title'),
                                                      read_only=True)
