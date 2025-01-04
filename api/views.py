from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Sum, F, Q
from .models import Grade, Book, Purchase, Wallet, Payment, CustomUser
from .serialayser import GradeSerializer, BookSerializer, PurchaseSerializer, WalletSerializer, PaymentSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def students_and_wallets(self, request, pk=None):
        grade = self.get_object()
        students = CustomUser.objects.filter(grade=grade)
        wallets = Wallet.objects.filter(student__in=students)

        student_data = [{
            'username': student.username,
            'email': student.email,
            'phone_number': student.phone_number,
        } for student in students]

        wallet_data = [{
            'student': wallet.student.username,
            'balance': wallet.balance,
        } for wallet in wallets]

        return Response({
            'students': student_data,
            'wallets': wallet_data,
            'total_students': students.count()
        })

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['get'])
    def detail_data(self, request, pk=None):
        book = self.get_object()

        # Calculate total sum of all purchases for this book
        total_sum = Purchase.objects.filter(book=book, is_paid=True).aggregate(total_sum=Sum('price_paid'))['total_sum'] or 0.00

        # Get all users who purchased this book and the quantity bought
        purchases = Purchase.objects.filter(book=book, is_paid=True)
        user_purchase_data = {}
        for purchase in purchases:
            user = purchase.student.username
            user_purchase_data[user] = user_purchase_data.get(user, 0) + purchase.quantity

        # Get the stock of the book
        stock = book.stock

        return Response({
            'total_sum': total_sum,
            'users': [{'user': user, 'quantity': quantity} for user, quantity in user_purchase_data.items()],
            'stock': stock
        })


class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Purchase.objects.filter(student=self.request.user)

    @action(detail=False, methods=['get'])
    def unpaid_purchases(self, request):
        user = request.user
        unpaid_purchases = (
            Purchase.objects.filter(student=user)
            .annotate(total_paid=Sum('payments__amount_paid'))
            .filter(Q(total_paid__lt=F('price_paid')) | Q(total_paid__isnull=True))
        )

        purchases_with_remaining = []
        for purchase in unpaid_purchases:
            remaining_amount = purchase.price_paid - (purchase.total_paid or 0)
            purchases_with_remaining.append({
                'purchase_id': purchase.id,
                'book': purchase.book.title,
                'remaining_amount': remaining_amount,
            })

        total_unpaid = sum(item['remaining_amount'] for item in purchases_with_remaining)

        return Response({
            'unpaid_purchases': purchases_with_remaining,
            'total_unpaid': total_unpaid,
        })

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)



# WalletViewSet
class WalletViewSet(viewsets.ReadOnlyModelViewSet):  # Read-only access for wallets
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Wallet.objects.filter(student=self.request.user)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(student=self.request.user)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
