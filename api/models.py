from django.contrib.auth.models import AbstractUser
from django.db import models

class Grade(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class School(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    date = models.DateField()

    def __str__(self):
        return self.name

class Category(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return self.title

class CustomUser(AbstractUser):
    grade = models.ForeignKey('Grade', on_delete=models.CASCADE, related_name='students', null=True, blank=True)    
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_activated = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.email

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='books/', blank=True, null=True)

    def __str__(self):
        return self.title

class Wallet(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

class Purchases(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    purchase_date = models.DateField()
    quantity = models.IntegerField()
    price_paid = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)

class Payment(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    purchase = models.ForeignKey(Purchases, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=1)
