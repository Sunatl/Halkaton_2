from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Grade, School, Category, CustomUser, Book, Wallet, Purchases, Payment
from .serialayser import *

class GradeListCreateView(ListCreateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name', 'description']
    ordering_fields = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        for grade in queryset:
            grade.total_students = grade.students.count()  # Истифодаи related_name
        return queryset

class GradeRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grade = self.get_object()
        context['students'] = grade.customuser_set.values('username', 'email', 'phone')
        return context

class SchoolListCreateView(ListCreateAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name', 'address']
    ordering_fields = ['name', 'date']

class SchoolRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

class CategoryListCreateView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['title']
    search_fields = ['title']
    ordering_fields = ['date']

class CategoryRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CustomUserListCreateView(ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['username', 'email', 'is_activated']
    search_fields = ['username', 'email', 'phone']
    ordering_fields = ['username', 'email']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return super().get_queryset()
        return CustomUser.objects.filter(id=user.id)

class CustomUserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return super().get_queryset()
        return CustomUser.objects.filter(id=user.id)

class BookListCreateView(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_available', 'is_deleted']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'stock']

    def get_queryset(self):
        queryset = super().get_queryset()
        for book in queryset:
            book.total_stock_value = book.price * book.stock
        return queryset

class BookRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        purchases = Purchases.objects.filter(book=book)
        context['purchases'] = purchases.values('student__username', 'quantity', 'price_paid')
        return context

class WalletListCreateView(ListCreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['student']
    search_fields = ['student__username']
    ordering_fields = ['balance']

class WalletRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

class PurchasesListCreateView(ListCreateAPIView):
    queryset = Purchases.objects.all()
    serializer_class = PurchasesSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['student', 'book']
    search_fields = ['student__username', 'book__title']
    ordering_fields = ['purchase_date', 'quantity']

class PurchasesRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Purchases.objects.all()
    serializer_class = PurchasesSerializer

class PaymentListCreateView(ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['student', 'status']
    search_fields = ['student__username', 'payment_method']
    ordering_fields = ['amount_paid', 'payment_date']

class PaymentRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
