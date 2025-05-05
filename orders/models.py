# orders/models.py
from django.db import models
from flowers.models import Bouquet
from constructor.models import CustomBouquet


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В обработке'),
        ('completed', 'Завершен'),
        ('canceled', 'Отменен'),
    ]

    # user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    session_key = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"Заказ #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    bouquet = models.ForeignKey(Bouquet, on_delete=models.SET_NULL, null=True, blank=True)
    custom_bouquet = models.ForeignKey(CustomBouquet, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        if self.bouquet:
            return f"{self.bouquet.name} x {self.quantity}"
        return f"Кастомный букет x {self.quantity}"