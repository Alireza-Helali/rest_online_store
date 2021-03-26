from django.conf import settings
from rest_framework.response import Response

from rest_framework import viewsets, generics, mixins, status
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.reverse import reverse

from .serializer import ProductSerializer, \
    ProductDetailSerializer, CommentSerializer, CategorySerializer, \
    SubcategorySerializer, SupplierSerializer, SupplierDetailSerializer, \
    SupplierProductSerializer, SupplierProductDetailSerializer, TagSerializer

from .models import Tag, Product, Comment, Category, SubCategory, Supplier
from .permissions import TagPermission
from account.permissions import SuperUserPermission


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductSerializer
        return ProductDetailSerializer


class CommentView(viewsets.GenericViewSet, mixins.ListModelMixin,
                  mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin
                  ):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(approved=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    # permission_classes = [SuperUserPermission]
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [SuperUserPermission]
        return super(CategoryView, self).get_permissions()


class SubcategoryView(viewsets.ModelViewSet):
    serializer_class = SubcategorySerializer
    queryset = SubCategory.objects.all()
    permission_classes = [SuperUserPermission]


class SupplierView(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        queryset = Product.objects.filter(supplier_id=pk)
        if not queryset:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = SupplierDetailSerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        queryset = Supplier.objects.all()
        if not queryset:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = SupplierSerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)


# class SupplierProductView(viewsets.ReadOnlyModelViewSet):
#     def get_queryset(self, pk=None):
#         if self.action == 'list':
#             return Supplier.objects.all()
#         else:
#             supplier_pk = self.kwargs.get('pk')
#             qs = Product.objects.filter(supplier_id=supplier_pk)
#             print(qs)
#             return qs
#
#     def get_serializer_class(self):
#         if self.action == 'list':
#             return SupplierSerializer
#         elif self.action == 'retrieve':
#             return SupplierDetailSerializer


# ------------------- Supplier CRUD System -------------------

class SupplierProductManageView(viewsets.ModelViewSet):
    """model view set for suppliers to add, delete and update a product"""

    def get_queryset(self):
        return Product.objects.filter(supplier__user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return SupplierProductSerializer
        else:
            return SupplierProductDetailSerializer


from django.db.models import Prefetch, Q


class SupplierTagView(generics.ListCreateAPIView):
    serializer_class = TagSerializer

    def get_queryset(self):
        return Tag.objects.filter(product__supplier__user=self.request.user). \
            prefetch_related(Prefetch('product', queryset=Product.objects.filter(supplier__user=self.request.user)))
