from rest_framework import routers
from .views import ProductViewSet, OrderViewSet, register, CartViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')
# Nota: CartViewSet no es un ModelViewSet registrado al router; lo exponemos manualmente abajo.

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', register, name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # rutas del carrito
    path('cart/', CartViewSet.as_view({'get': 'list'}), name='cart'),
    path('cart/add/', CartViewSet.as_view({'post': 'add'}), name='cart-add'),
    path('cart/remove/', CartViewSet.as_view({'post': 'remove'}), name='cart-remove'),
    path('cart/clear/', CartViewSet.as_view({'post': 'clear'}), name='cart-clear'),
    path('cart/checkout/', CartViewSet.as_view({'post': 'checkout'}), name='cart-checkout'),
]