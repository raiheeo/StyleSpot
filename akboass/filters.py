from django_filters import FilterSet
from .models import User, Product, Category, Cart, CartItem


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {

            'price': ['gt', 'lt'],
            'color': ['exact'],
            'category': ['exact'],
            'size': ['gt', 'lt'],

       }


class SaleFilter(FilterSet):
    class Meta:
        model = Category
        fields = {
            'sale': ['exact']
        }