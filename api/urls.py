from django.urls import path
from .views import (
    GradeListCreateView, GradeRetrieveUpdateDestroyView,
    SchoolListCreateView, SchoolRetrieveUpdateDestroyView,
    CategoryListCreateView, CategoryRetrieveUpdateDestroyView,
    CustomUserListCreateView, CustomUserRetrieveUpdateDestroyView,
    BookListCreateView, BookRetrieveUpdateDestroyView,
    WalletListCreateView, WalletRetrieveUpdateDestroyView,
    PurchasesListCreateView, PurchasesRetrieveUpdateDestroyView,
    PaymentListCreateView, PaymentRetrieveUpdateDestroyView
)

urlpatterns = [
    path('grades/', GradeListCreateView.as_view(), name='grade-list-create'),
    path('grades/<int:pk>/', GradeRetrieveUpdateDestroyView.as_view(), name='grade-detail'),

    path('schools/', SchoolListCreateView.as_view(), name='school-list-create'),
    path('schools/<int:pk>/', SchoolRetrieveUpdateDestroyView.as_view(), name='school-detail'),

    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-detail'),

    path('users/', CustomUserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', CustomUserRetrieveUpdateDestroyView.as_view(), name='user-detail'),

    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookRetrieveUpdateDestroyView.as_view(), name='book-detail'),

    path('wallets/', WalletListCreateView.as_view(), name='wallet-list-create'),
    path('wallets/<int:pk>/', WalletRetrieveUpdateDestroyView.as_view(), name='wallet-detail'),

    path('purchases/', PurchasesListCreateView.as_view(), name='purchases-list-create'),
    path('purchases/<int:pk>/', PurchasesRetrieveUpdateDestroyView.as_view(), name='purchases-detail'),

    path('payments/', PaymentListCreateView.as_view(), name='payment-list-create'),
    path('payments/<int:pk>/', PaymentRetrieveUpdateDestroyView.as_view(), name='payment-detail'),
]
