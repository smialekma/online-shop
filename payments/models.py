from datetime import datetime
from decimal import Decimal

from django.db import models
from django.utils import timezone

from orders.models import Order


class Payment(models.Model):
    stripe_checkout_id: str | models.CharField = models.CharField()
    order: models.ForeignKey = models.ForeignKey(
        Order,
        related_name="payments",
        on_delete=models.CASCADE,
    )
    amount: float | Decimal | models.DecimalField = models.DecimalField(
        decimal_places=2, max_digits=8
    )
    payment_method: str | models.CharField = models.CharField(null=True, blank=True)
    is_paid: bool | models.BooleanField = models.BooleanField(default=False)
    created_at: datetime | models.DateTimeField = models.DateTimeField(
        default=timezone.now
    )

    def get_status_for_display(self) -> str:
        if self.is_paid:
            return "Paid"
        else:
            return "Unpaid"
