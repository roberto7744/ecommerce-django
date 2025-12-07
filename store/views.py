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

class ProductViewSet(viewsets.ModelViewSet):
    """CRUD de productos."""
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class OrderViewSet(viewsets.ModelViewSet):
    """CRUD de pedidos (admin o usuario)."""
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer

    def get_permissions(self):
        # sólo autenticados pueden crear/consultar sus pedidos; admin puede todo
        if self.action in ['create', 'retrieve', 'list']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def perform_create(self, serializer):
        items = serializer.validated_data.get('items', [])
        total = sum([float(item.get('price', 0)) * int(item.get('quantity', 1)) for item in items])
        serializer.save(user=self.request.user, total=total)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    """Registro simple de usuario."""
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    # crear carrito vacío al registrar el usuario
    Cart.objects.create(user=user)
    return Response({"username": user.username, "email": user.email}, status=201)


class CartViewSet(viewsets.ViewSet):
    """Operaciones sobre el carrito: ver, add, remove, clear, checkout."""
    permission_classes = [permissions.IsAuthenticated]

    def get_cart(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart

    def list(self, request):
        """GET /api/cart/  -> devuelve el carrito del usuario."""
        cart = self.get_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add(self, request):
        """POST /api/cart/add/  body: {product_id, quantity}"""
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Producto no encontrado."}, status=404)
        if product.stock < quantity:
            return Response({"detail": "Stock insuficiente."}, status=400)
        cart = self.get_cart(request)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': quantity})
        if not created:
            item.quantity += quantity
            item.save()
        return Response({"detail": "Producto añadido al carrito."}, status=201)

    @action(detail=False, methods=['post'])
    def remove(self, request):
        """POST /api/cart/remove/ body: {product_id} -> elimina item del carrito"""
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({"detail": "product_id requerido."}, status=400)
        cart = self.get_cart(request)
        removed = CartItem.objects.filter(cart=cart, product_id=product_id).delete()
        if removed[0] == 0:
            return Response({"detail": "Item no encontrado en carrito."}, status=404)
        return Response({"detail": "Item eliminado."}, status=200)

    @action(detail=False, methods=['post'])
    def clear(self, request):
        """POST /api/cart/clear/ -> vacía carrito"""
        cart = self.get_cart(request)
        CartItem.objects.filter(cart=cart).delete()
        return Response({"detail": "Carrito vaciado."}, status=200)

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        """POST /api/cart/checkout/ -> crea un Order, deduce stock y vacía carrito."""
        cart = self.get_cart(request)
        items = list(cart.items.select_related('product').all())

        if not items:
            return Response({"detail": "Carrito vacío."}, status=400)

        # Validar stock antes y aplicar en una transacción
        with transaction.atomic():
            # bloquear productos para evitar race conditions
            product_ids = [it.product.pk for it in items]
            products = Product.objects.select_for_update().filter(pk__in=product_ids)
            product_map = {p.pk: p for p in products}

            order_items = []
            total = 0.0
            for it in items:
                prod = product_map.get(it.product.pk)
                if prod is None:
                    return Response({"detail": f"Producto {it.product.pk} no existe."}, status=400)
                if prod.stock < it.quantity:
                    return Response({"detail": f"Stock insuficiente para {prod.name}."}, status=400)
                # calcular precio y restar stock
                line_total = float(prod.price) * int(it.quantity)
                total += line_total
                order_items.append({
                    "product_id": prod.pk,
                    "name": prod.name,
                    "price": str(prod.price),
                    "quantity": it.quantity
                })
                prod.stock = prod.stock - it.quantity
                prod.save()

            # crear order
            order = Order.objects.create(user=request.user, items=order_items, total=total, status='PAID')
            # vaciar carrito
            CartItem.objects.filter(cart=cart).delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=201)