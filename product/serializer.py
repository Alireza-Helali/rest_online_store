from rest_framework import serializers
from .models import Tag, Product, Comment, Category, SubCategory, Supplier


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = (
            'image', 'name', 'price', 'url'
        )


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['user', 'product', 'body', 'created']


class ProductDetailSerializer(serializers.ModelSerializer):
    supplier = serializers.StringRelatedField()
    subcategory = serializers.StringRelatedField()
    tags = serializers.StringRelatedField(many=True)
    comment_number = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True)

    def get_comment_number(self, obj):
        return obj.comments.all().count()

    class Meta:
        model = Product
        fields = (
            'name', 'description', 'price', 'image',
            'quantity', 'subcategory', 'supplier', 'url',
            'tags', 'comment_number', 'comments'
        )


class CategorySerializer(serializers.ModelSerializer):
    subcategory = serializers.HyperlinkedRelatedField(many=True, view_name='subcategory-detail', read_only=True)

    class Meta:
        model = Category
        fields = ['title', 'subcategory']


class SubcategorySerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()

    def get_category_name(self, obj):
        return obj.category.title

    class Meta:
        model = SubCategory
        fields = ['category', 'category_name', 'title']
        extra_kwargs = {'category': {'write_only': True}}


class SupplierSerializer(serializers.HyperlinkedModelSerializer):
    product_number = serializers.SerializerMethodField()

    def get_product_number(self, obj):
        return Product.objects.filter(supplier__store_name=obj).count()

    class Meta:
        model = Supplier
        fields = ['store_name', 'product_number', 'url']


class SupplierDetailSerializer(serializers.ModelSerializer):
    supplier = serializers.StringRelatedField()
    subcategory = serializers.StringRelatedField()
    tags = serializers.StringRelatedField(many=True)
    comment_number = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True)

    def get_comment_number(self, obj):
        return obj.comments.all().count()

    class Meta:
        model = Product
        fields = (
            'name', 'description', 'price', 'image',
            'quantity', 'subcategory', 'supplier', 'url',
            'tags', 'comment_number', 'comments'
        )


# ---------------- Supplier CRUD system -----------------


class SupplierProductSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='manager-detail')

    class Meta:
        model = Product
        fields = (
            'image', 'name', 'price', 'url'
        )


class SupplierProductDetailSerializer(serializers.ModelSerializer):
    supplier = serializers.StringRelatedField(read_only=True)
    subcategory = serializers.StringRelatedField()
    tags = serializers.StringRelatedField(many=True)
    comment_number = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    def get_comment_number(self, obj):
        return obj.comments.all().count()

    class Meta:
        model = Product
        fields = (
            'name', 'description', 'price', 'image',
            'quantity', 'subcategory', 'supplier',
            'tags', 'comment_number', 'comments'
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['title', 'product']
