from django.db import models
from django.utils import timezone

from orders.models import Order


class Payment(models.Model):
    stripe_checkout_id = models.CharField()
    order = models.ForeignKey(
        Order,
        related_name="payments",
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(decimal_places=2, max_digits=8)
    payment_method = models.CharField(null=True, blank=True)
    status = models.CharField()
    created_at = models.DateTimeField(default=timezone.now)
