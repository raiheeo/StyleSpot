from .models import Category, Product, Support, User, Cart, CartItem
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname', 'user_image']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name', 'sale']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'product_image', 'old_price', 'price', 'size',
                  'description', 'category', 'quantity', 'material', 'stock', ]

class SupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Support
        fields = ['name', 'email', 'phone_number', 'comment', 'comment_image']


class CartItemSerializer(serializers.Serializer):
    title_id = serializers.CharField(max_length=100)  # ID товара
    quantity = serializers.IntegerField(min_value=1, default=1)  # Количество

class CartSerializer(serializers.Serializer):
    total_items = serializers.SerializerMethodField()  # Общее количество товаров

    def get_total_items(self, obj):
        return sum(item['quantity'] for item in obj['items'])




