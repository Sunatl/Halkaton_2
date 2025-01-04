from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.exceptions import ValidationError


class Grade(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True, related_name="students")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username} ({self.grade.name if self.grade else 'No Grade'})"


class Wallet(models.Model):
    student = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="wallet")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Wallet of {self.student.username} - {self.balance} сомонӣ"

    def add_balance(self, amount):
        if amount < 0:
            raise ValueError("Маблағ бояд мусбӣ бошад!")
        self.balance += amount
        self.save()

    def subtract_balance(self, amount):
        if amount < 0:
            raise ValueError("Маблағ бояд мусбӣ бошад!")
        if self.balance >= amount:
            self.balance -= amount
            self.save()
        else:
            raise ValueError("Маблағи кофӣ дар ҳисоби талабагӣ нест!")

    def has_enough_balance(self, amount):
        return self.balance >= amount

    def get_transaction_history(self):
        return self.transactions.all()

    def reset_balance(self):
        self.balance = 0
        self.save()


@receiver(post_save, sender=CustomUser)
def create_wallet_for_user(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(student=instance, balance=0)


class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def reduce_stock(self, quantity):
        if self.stock >= quantity:
            self.stock -= quantity
            self.is_available = self.stock > 0
            self.save()
        else:
            raise ValueError("Китоб кофӣ нест дар саҳом!")

    def is_in_stock(self):
        return self.stock > 0
class Purchase(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="purchases")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="purchases")
    purchase_date = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)
    price_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.username} - {self.book.title} ({'Paid' if self.is_paid else 'Not Paid'})"

    @transaction.atomic
    def make_purchase(self):
        total_price = self.quantity * self.book.price
        if self.book.stock < self.quantity:
            raise ValueError("Китоб кофӣ нест дар саҳом!")
        if not self.student.wallet.has_enough_balance(total_price):
            raise ValueError("Маблағи кофӣ дар ҳисоби талабагӣ нест!")
        self.book.reduce_stock(self.quantity)
        self.student.wallet.subtract_balance(total_price)
        self.price_paid = total_price
        self.is_paid = True
        self.save()
        self.create_payment()


    @transaction.atomic
    def pay(self):
        # Ensure the purchase has not been paid before
        if self.is_paid:
            raise ValueError("Харид аллакай пардохт шудааст!")

        # Ensure the student has enough balance in the wallet
        if not self.student.wallet.has_enough_balance(self.price_paid):
            raise ValueError("Маблағи кофӣ дар ҳисоби талабагӣ нест!")

        # Subtract the amount from the wallet
        self.student.wallet.subtract_balance(self.price_paid)

        # Mark the purchase as paid
        self.is_paid = True
        self.save()

        # Create the payment record
        self.create_payment()

    def create_payment(self):
        if not self.is_paid:
            raise ValueError("Харид то ҳол пардохт нашудааст!")

        # Create the payment instance
        payment = Payment.objects.create(
            student=self.student,
            purchase=self,
            amount_paid=self.price_paid,
            payment_method='card',  # Example payment method
            status='completed'
        )

        return payment




class Payment(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="payments")
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="payments")
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, choices=[('cash', 'Cash'), ('card', 'Card'), ('online', 'Online')])
    status = models.CharField(max_length=20, choices=[('completed', 'Completed'), ('failed', 'Failed'), ('pending', 'Pending')], default='pending')

    def __str__(self):
        return f"Payment of {self.amount_paid} by {self.student.username} for {self.purchase.book.title} on {self.payment_date}"
    def save(self, *args, **kwargs):
        if self.status == 'completed':
            raise ValueError("Пардохт аллакай анҷом шудааст!")
        if self.student.wallet.has_enough_balance(self.amount_paid):
            self.student.wallet.subtract_balance(self.amount_paid)
            self.status = 'completed'
        else:
            self.status = 'failed'
        super().save(*args, **kwargs)


    def create_payment(self):
        if Payment.objects.filter(purchase=self).exists():
            raise ValueError("Пардохт аллакай мавҷуд аст!")
        if not self.is_paid:
            raise ValueError("Харид то ҳол пардохт нашудааст!")
        return Payment.objects.create(
            student=self.student,
            purchase=self,
            amount_paid=self.price_paid,
            payment_method='card',
            status='completed'
        )

