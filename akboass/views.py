from rest_framework import viewsets, permissions, status
from .models import Category, Product, Support, User, Cart, CartItem
from .serializers import CategorySerializer, SupportSerializer, ProductSerializer, UserSerializer, CartSerializer, CartItemSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action


class ProductListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        movies = Product.objects.all()
        serializer = ProductSerializer(movies, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class SupportViewSet(viewsets.ModelViewSet):
    queryset = Support.objects.all()
    serializer_class = SupportSerializer
    permission_classes = [permissions.AllowAny]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class CartViewSet(viewsets.ModelViewSet):
    """
    Простой ViewSet для корзины товаров.
    """
    # Хранилище для данных корзины (можно заменить на базу данных)
    cart = {}

    def list(self, request):
        """
        Обработчик GET-запроса для получения содержимого корзины.
        """
        return Response({"cart": self.cart})

    def retrieve(self, request, pk=None):
        """
        Обработчик GET-запроса для получения данных о конкретном товаре в корзине.
        """
        item = self.cart.get(pk)
        if not item:
            return Response({"error": f"Товар с ID {pk} не найден в корзине"}, status=404)
        return Response({"item": item})

    def create(self, request):
        """
        Обработчик POST-запроса для добавления товара в корзину.
        """
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)
        
        if not product_id:
            return Response({"error": "Не указан product_id"}, status=400)
        
        # Добавляем товар в корзину
        if product_id in self.cart:
            self.cart[product_id]["quantity"] += quantity
        else:
            self.cart[product_id] = {"product_id": product_id, "quantity": quantity}

        return Response({"message": "Товар добавлен в корзину", "cart": self.cart})

    def destroy(self, request, pk=None):
        """
        Обработчик DELETE-запроса для удаления товара из корзины.
        """
        if pk in self.cart:
            del self.cart[pk]
            return Response({"message": f"Товар с ID {pk} удалён из корзины"})
        return Response({"error": f"Товар с ID {pk} не найден в корзине"}, status=404)

    @action(detail=False, methods=["delete"])
    def clear(self, request):
        """
        Кастомное действие для очистки всей корзины.
        """
        self.cart.clear()
        return Response({"message": "Корзина очищена"})