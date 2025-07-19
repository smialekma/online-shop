from django.db import models

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
    is_payed = models.BooleanField()
    date_ordered = models.DateTimeField()
    date_fulfilled = models.DateTimeField()
    address = models.ForeignKey(
        CustomerAddress,
        related_name="orders",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    total_amount = models.DecimalField(decimal_places=2, max_digits=8)
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
