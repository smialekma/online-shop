from decimal import Decimal

from django.db import models
from django.utils import timezone

from customers.models import Customer
from customer_addresses.models import CustomerAddress


class ShippingMethod(models.Model):
    name = models.CharField()
    price = models.DecimalField(decimal_places=2, max_digits=5)
    min_delivery_time_in_days = models.IntegerField()
    max_delivery_time_in_days = models.IntegerField()

    def __str__(self):
        return self.name

    def get_delivery_time_for_display(self) -> str:
        if self.max_delivery_time_in_days == self.min_delivery_time_in_days:
            return f"{self.min_delivery_time_in_days} day(s)"
        else:
            return f"{self.min_delivery_time_in_days} - {self.max_delivery_time_in_days} days"


class Order(models.Model):
    customer = models.ForeignKey(
        Customer,
        related_name="orders",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
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
    shipping_method = models.ForeignKey(
        ShippingMethod,
        related_name="orders",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    @property
    def is_paid(self):
        return self.payments and self.payments.filter(is_paid=True).exists()

    def get_status_for_display(self) -> str:
        if self.is_paid:
            return "Paid"
        else:
            return "Unpaid"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name="order_items", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        "products.Product",
        related_name="order_items",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    quantity = models.IntegerField()

    def get_subtotal(self) -> Decimal:
        return Decimal(self.quantity * self.product.price)


# Order.order_items.all() order_items -> product.
