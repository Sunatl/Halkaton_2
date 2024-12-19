from rest_framework import serializers
from .models import Grade, School, Category, CustomUser, Book, Wallet, Purchases, Payment

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['id', 'name', 'description']

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'name', 'address', 'phone_number', 'date']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'date']

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'grade', 'phone', 'is_activated', 'category', 'school']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'price', 'stock', 'is_available', 'is_deleted', 'deleted_at', 'image']

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'student', 'balance']

class PurchasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchases
        fields = ['id', 'student', 'book', 'purchase_date', 'quantity', 'price_paid', 'is_paid']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'student', 'purchase', 'amount_paid', 'payment_date', 'payment_method', 'status']
