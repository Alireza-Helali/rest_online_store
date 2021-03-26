from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import ProductViewSet, CommentView, CategoryView, \
    SubcategoryView, SupplierView, SupplierProductManageView, SupplierTagView

router = DefaultRouter()

router.register('product', ProductViewSet, basename='product')
router.register('comment', CommentView, basename='comment')
router.register('category', CategoryView, basename='category')
router.register('subcategory', SubcategoryView, basename='subcategory')
router.register('supplier', SupplierView, basename='supplier')
router.register('supp-manage', SupplierProductManageView, basename='manager')

urlpatterns = [
    path('', include(router.urls)),
    path('tags', SupplierTagView.as_view(), name='tag'),
]
