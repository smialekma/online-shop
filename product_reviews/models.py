from django.db import models

from customers.models import Customer
from products.models import Product


class Review(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    rating = models.IntegerField()
    user_id = models.ForeignKey(
        Customer,
        related_name="reviews",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    product_id = models.ForeignKey(
        Product, related_name="reviews", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField()
