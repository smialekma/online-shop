from datetime import datetime
from decimal import Decimal

from django.db import models
from django.utils import timezone

from customers.models import Customer
from customer_addresses.models import CustomerAddress


class ShippingMethod(models.Model):
    name: str | models.CharField = models.CharField()
    price: float | Decimal | models.DecimalField = models.DecimalField(
        decimal_places=2, max_digits=5
    )
    min_delivery_time_in_days: int | models.IntegerField = models.IntegerField()
    max_delivery_time_in_days: int | models.IntegerField = models.IntegerField()

    def __str__(self) -> str:
        return self.name

    def get_delivery_time_for_display(self) -> str:
        if self.max_delivery_time_in_days == self.min_delivery_time_in_days:
            return f"{self.min_delivery_time_in_days} day(s)"
        else:
            return f"{self.min_delivery_time_in_days} - {self.max_delivery_time_in_days} days"


class Order(models.Model):
    customer: models.ForeignKey = models.ForeignKey(
        Customer,
        related_name="orders",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    date_ordered: datetime | models.DateTimeField = models.DateTimeField(
        default=timezone.now
    )
    date_fulfilled: datetime | models.DateTimeField = models.DateTimeField(
        blank=True, null=True
    )
    address: models.ForeignKey = models.ForeignKey(
        CustomerAddress,
        related_name="orders",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    created_at: datetime | models.DateTimeField = models.DateTimeField(
        default=timezone.now
    )
    updated_at: datetime | models.DateTimeField = models.DateTimeField(
        blank=True, null=True
    )
    total_amount: float | Decimal | models.DecimalField = models.DecimalField(
        decimal_places=2, max_digits=8
    )
    order_notes: str | models.TextField = models.TextField(
        max_length=300, blank=True, null=True
    )
    email: str | models.EmailField = models.EmailField()
    shipping_method: models.ForeignKey = models.ForeignKey(
        ShippingMethod,
        related_name="orders",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    @property
    def is_paid(self) -> bool:
        return self.payments.exists() and self.payments.filter(is_paid=True).exists()

    def get_status_for_display(self) -> str:
        if self.is_paid:
            return "Paid"
        else:
            return "Unpaid"


class OrderItem(models.Model):
    order: models.ForeignKey = models.ForeignKey(
        Order, related_name="order_items", on_delete=models.CASCADE
    )
    product: models.ForeignKey = models.ForeignKey(
        "products.Product",
        related_name="order_items",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    quantity: int | models.IntegerField = models.IntegerField()

    def get_subtotal(self) -> Decimal:
        return Decimal(self.quantity * self.product.price)


# Order.order_items.all() order_items -> product.
