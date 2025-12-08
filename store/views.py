# store/views.py (Versión Corregida Definitiva)
# pylint: disable=E1101

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db import transaction

from .models import Product, Order, Cart, CartItem
from .serializers import (
    ProductSerializer, OrderSerializer, RegisterSerializer,
    CartSerializer, CartItemSerializer
)

# ---------------------------------------------------------
# PRODUCTOS
# ---------------------------------------------------------

class ProductViewSet(viewsets.ModelViewSet):
    """CRUD de productos."""
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


# ---------------------------------------------------------
# ÓRDENES
# ---------------------------------------------------------

class OrderViewSet(viewsets.ModelViewSet):
    """CRUD de pedidos (admin o usuario)."""
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.action in ['create', 'retrieve', 'list']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def perform_create(self, serializer):
        items = serializer.validated_data.get('items', [])
        total = sum([float(item.get('price', 0)) * int(item.get('quantity', 1)) for item in items])
        serializer.save(user=self.request.user, total=total)


# ---------------------------------------------------------
# REGISTRO
# ---------------------------------------------------------

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    """Registro simple de usuario."""
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    # Crear carrito vacío
    Cart.objects.create(user=user)

    return Response(
        {"username": user.username, "email": user.email},
        status=status.HTTP_201_CREATED
    )


# ---------------------------------------------------------
# CARRITO
# ---------------------------------------------------------

class CartViewSet(viewsets.ViewSet):
    """Operaciones sobre el carrito: ver, add, remove, clear, checkout."""
    permission_classes = [permissions.IsAuthenticated]

    def get_cart(self, request):
        """Garantiza que el carrito existe."""
        cart, created = Cart.objects.get_or_create(user=request.user)
        return cart

    # -------------------------------
    # GET /api/cart/
    # -------------------------------
    def list(self, request):
        """Devuelve el carrito del usuario autenticado."""

        if not request.user.is_authenticated:
            return Response(
                {"detail": "Credenciales inválidas."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            cart = self.get_cart(request)

            # Serializamos items adecuadamente
            items = CartItem.objects.filter(cart=cart).select_related("product")
            data = {
                "id": cart.id,
                "user": cart.user.username,
                "items": CartItemSerializer(items, many=True).data
            }

            return Response(data)

        except Exception as e:
            return Response(
                {"detail": f"Error interno al obtener el carrito: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # -------------------------------
    # POST /api/cart/add/
    # -------------------------------
    @action(detail=False, methods=['post'])
    def add(self, request):
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data["product_id"]
        quantity = serializer.validated_data["quantity"]

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Producto no encontrado."}, status=404)

        if product.stock < quantity:
            return Response({"detail": "Stock insuficiente."}, status=400)

        cart = self.get_cart(request)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": quantity}
        )

        if not created:
            item.quantity += quantity
            item.save()

        return Response(
            {"detail": "Producto añadido al carrito."},
            status=status.HTTP_201_CREATED
        )

    # -------------------------------
    # POST /api/cart/remove/
    # -------------------------------
    @action(detail=False, methods=['post'])
    def remove(self, request):
        product_id = request.data.get("product_id")

        if not product_id:
            return Response({"detail": "product_id requerido."}, status=400)

        cart = self.get_cart(request)

        deleted = CartItem.objects.filter(cart=cart, product_id=product_id).delete()

        if deleted[0] == 0:
            return Response({"detail": "Item no encontrado."}, status=404)

        return Response({"detail": "Item eliminado."}, status=200)

    # -------------------------------
    # POST /api/cart/clear/
    # -------------------------------
    @action(detail=False, methods=['post'])
    def clear(self, request):
        cart = self.get_cart(request)
        CartItem.objects.filter(cart=cart).delete()
        return Response({"detail": "Carrito vaciado."})

    # -------------------------------
    # POST /api/cart/checkout/
    # -------------------------------
    @action(detail=False, methods=['post'])
    def checkout(self, request):
        cart = self.get_cart(request)
        items = list(cart.items.select_related("product").all())

        if not items:
            return Response({"detail": "Carrito vacío."}, status=400)

        with transaction.atomic():
            product_ids = [i.product.id for i in items]
            products = Product.objects.select_for_update().filter(id__in=product_ids)
            product_map = {p.id: p for p in products}

            order_items = []
            total = 0.0

            for i in items:
                prod = product_map.get(i.product.id)

                if prod.stock < i.quantity:
                    return Response(
                        {"detail": f"Stock insuficiente para {prod.name}."},
                        status=400
                    )

                line_total = float(prod.price) * i.quantity
                total += line_total

                order_items.append({
                    "product_id": prod.id,
                    "name": prod.name,
                    "price": str(prod.price),
                    "quantity": i.quantity
                })

                prod.stock -= i.quantity
                prod.save()

            order = Order.objects.create(
                user=request.user,
                items=order_items,
                total=total,
                status="PAID"
            )

            CartItem.objects.filter(cart=cart).delete()

        return Response(OrderSerializer(order).data, status=201)
