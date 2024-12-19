from rest_framework import serializers
from .models import Grade, School, Category, CustomUser, Book, Wallet, Purchases, Payment
from rest_framework import serializers
from api.models import CustomUser

from rest_framework import serializers
from django.contrib.auth import authenticate
from api.models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'grade', 'category', 'school', 'password', 'password_confirm']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

class GradeSerializer(serializers.ModelSerializer):
    students = RegisterSerializer(many=True, read_only=True)  # Истифодаи related_name бевосита

    class Meta:
        model = Grade
        fields = ['id', 'name', 'description', 'students']


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'name', 'address', 'phone_number', 'date']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'date']


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
        return user
    



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
