from rest_framework import viewsets, permissions, status
from .models import Category, Product, Support, User, Cart, CartItem
from .serializers import CategorySerializer, SupportSerializer, ProductSerializer, UserSerializer, CartSerializer, CartItemSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter, SaleFilter



class ProductListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ['title']
    filterset_class = ['category', 'size', 'color', 'price']

    def get(self, request):
        product = Product.objects.all()
        serializer = ProductSerializer(Product, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    permission_classes = [permissions.AllowAny]
    ordering_fields = ['category_name', 'sale']
    search_fields = ['category_name']

class SupportViewSet(viewsets.ModelViewSet):
    queryset = Support.objects.all()
    serializer_class = SupportSerializer
    permission_classes = [permissions.AllowAny]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ['title']
    filterset_class = ProductFilter

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class CartViewSet(viewsets.ModelViewSet):
    cart = {}

    def list(self, request):
        return Response({"cart": self.cart})

    def retrieve(self, request, pk=None):
        item = self.cart.get(pk)
        if not item:
            return Response({"error": f"Товар с ID {pk} не найден в корзине"}, status=404)
        return Response({"item": item})

    def create(self, request):
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)
        
        if not product_id:
            return Response({"error": "Не указан product_id"}, status=400)
        
        if product_id in self.cart:
            self.cart[product_id]["quantity"] += quantity
        else:
            self.cart[product_id] = {"product_id": product_id, "quantity": quantity}

        return Response({"message": "Товар добавлен в корзину", "cart": self.cart})

    def destroy(self, request, pk=None):
        if pk in self.cart:
            del self.cart[pk]
            return Response({"message": f"Товар с ID {pk} удалён из корзины"})
        return Response({"error": f"Товар с ID {pk} не найден в корзине"}, status=404)

    @action(detail=False, methods=["delete"])
    def clear(self, request):
        self.cart.clear()
        return Response({"message": "Корзина очищена"})