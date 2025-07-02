from django.utils import timezone

from django.db import models

from customers.models import Customer
from products.models import Product


class Review(models.Model):
    # TODO rating choice field
    title = models.CharField(max_length=100)
    body = models.TextField()
    rating = models.IntegerField()
    author = models.ForeignKey(
        Customer,
        related_name="reviews",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    product = models.ForeignKey(
        Product, related_name="reviews", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
