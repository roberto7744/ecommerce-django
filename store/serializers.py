from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, Order, Cart, CartItem
from django.contrib.auth.password_validation import validate_password

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('created_at',)

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("El precio debe ser mayor o igual a 0.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("El stock no puede ser negativo.")
        return value


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'product_id', 'quantity')
        read_only_fields = ('id', 'product')

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("La cantidad debe ser al menos 1.")
        return value


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, source='items')

    class Meta:
        model = Cart
        fields = ('id', 'user', 'items')
        read_only_fields = ('id', 'user')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('user', 'total', 'status', 'created_at')