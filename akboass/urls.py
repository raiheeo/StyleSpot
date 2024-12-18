from django.urls import path, include
from .views import ProductListView
from .views import CategoryViewSet, SupportViewSet, ProductViewSet, UserViewSet, CartViewSet
from rest_framework.routers import DefaultRouter, SimpleRouter
from django.contrib import admin


router = SimpleRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'support', SupportViewSet)
router.register(r'product', ProductViewSet)
router.register(r'users', UserViewSet)



urlpatterns = [
    path('', include(router.urls)), # Подключение роутера
    path('cart/', CartViewSet.as_view({'get': 'list'}), name='cart-list'),
    path('cart/add/', CartViewSet.as_view({'post': 'add_item'}), name='cart-add'),
    path('cart/remove/<int:pk>/', CartViewSet.as_view({'delete': 'remove_item'}), name='cart-remove'),
]
