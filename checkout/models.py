from django.db import models
from django.utils import timezone

from userbase.models import User
from main.models import Product


class Order(models.Model):
    CART = 1
    PROCESSING = 2
    COMPLETED = 3
    CANCELLED = 4
    STATUS_CHOICES = [
        (CART, 'In Cart'),
        (PROCESSING, 'Being Processed'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.IntegerField(choices=STATUS_CHOICES, default=CART)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order {self.id} - {self.user.username} - {self.get_status_display()}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('main.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
