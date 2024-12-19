from django.contrib import admin
from .models import *

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone_number', 'date')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'is_activated', 'grade', 'category', 'school')
    search_fields = ('email', 'username')
    list_filter = ('is_activated', 'grade', 'school')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'stock', 'is_available', 'is_deleted')
    list_filter = ('is_available', 'is_deleted')

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('student', 'balance')

@admin.register(Purchases)
class PurchasesAdmin(admin.ModelAdmin):
    list_display = ('student', 'book', 'purchase_date', 'quantity', 'price_paid', 'is_paid')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'purchase', 'amount_paid', 'payment_date', 'payment_method', 'status')
