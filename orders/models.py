from django.db import models
from django.utils import timezone

from customers.models import Customer
from customer_addresses.models import CustomerAddress


class Order(models.Model):
    customer = models.ForeignKey(
        Customer,
        related_name="orders",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    is_payed = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(default=timezone.now)
    date_fulfilled = models.DateTimeField(blank=True, null=True)
    address = models.ForeignKey(
        CustomerAddress,
        related_name="orders",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True)
    total_amount = models.DecimalField(decimal_places=2, max_digits=8)
    order_notes = models.TextField(max_length=300, blank=True, null=True)
    email = models.EmailField()
    # shipping_tracker = models.TextField()


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name="order_items", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        "products.Product",
        related_name="orders",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    quantity = models.IntegerField()
