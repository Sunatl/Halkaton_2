from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GradeViewSet, BookViewSet, PurchaseViewSet, WalletViewSet, PaymentViewSet

router = DefaultRouter()
router.register(r'grades', GradeViewSet, basename='grade')
router.register(r'books', BookViewSet, basename='book')
router.register(r'purchases', PurchaseViewSet, basename='purchase')
router.register(r'wallets', WalletViewSet, basename='wallet')
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('api/', include(router.urls)),
]

