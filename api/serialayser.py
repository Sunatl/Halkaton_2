from rest_framework import serializers
from .models import Grade, Wallet, Book, Purchase, Payment, CustomUser
from django.contrib.auth import authenticate

# Serializer for Grade
class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['name', 'description']
        extra_kwargs = {
            'name': {'required': True},
            'description': {'required': False}
        }

# Serializer for Wallet (only for adding/removing balance)
class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['balance']  # Limiting to only show balance for API interactions

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'description', 'price', 'stock', 'is_available']
        extra_kwargs = {
            'title': {'required': True},
            'description': {'required': False},
            'price': {'required': True},
            'stock': {'required': True},
            'is_available': {'required': False}
        }
from rest_framework import serializers
from .models import Purchase

from rest_framework import serializers
from .models import Purchase

class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['book', 'quantity']
        extra_kwargs = {
            'book': {'required': True},
            'quantity': {'required': True, 'min_value': 1},
        }


    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("The quantity must be a positive number.")
        return value
class PaymentSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    purchase = serializers.PrimaryKeyRelatedField(queryset=Purchase.objects.all())

    class Meta:
        model = Payment
        fields = ['student', 'purchase', 'payment_method', 'amount_paid', 'status']
        extra_kwargs = {
            'student': {'required': True},
            'purchase': {'required': True},
            'payment_method': {'required': True},
            'amount_paid': {'required': True},
            'status': {'read_only': True}
        }

    def validate(self, data):
        purchase = data['purchase']
        if data['amount_paid'] != purchase.price_paid:
            raise serializers.ValidationError("Amount paid does not match the purchase price.")
        if not purchase.student.wallet.has_enough_balance(data['amount_paid']):
            raise serializers.ValidationError("Insufficient wallet balance for this payment.")
        return data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'grade', 'password', 'password_confirm']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = CustomUser.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, style={'input_type': 'password'})

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError({"detail": "Invalid username or password"})
        return data
