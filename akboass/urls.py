from django.urls import path, include
from .views import ProductListView
from .views import CategoryViewSet, SupportViewSet, ProductViewSet, UserViewSet, CartViewSet
from rest_framework.routers import DefaultRouter
from django.contrib import admin


router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'support', SupportViewSet)
router.register(r'products', ProductViewSet)
router.register(r'users', UserViewSet)



urlpatterns = [
    path('', include(router.urls)), # Подключение роутера
    path('product/', ProductListView.as_view(), name='product-list'),
    path('cart/', CartViewSet.as_view({'get': 'list'}), name='cart-list'),
    path('cart/add/', CartViewSet.as_view({'post': 'add_item'}), name='cart-add'),
    path('cart/remove/<int:pk>/', CartViewSet.as_view({'delete': 'remove_item'}), name='cart-remove'),
]
