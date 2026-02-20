from datetime import datetime

from django.utils import timezone

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from customers.models import Customer
from products.models import Product


class Review(models.Model):
    RATING_CHOICES = (
        (5, "star5"),
        (4, "star4"),
        (3, "star3"),
        (2, "star2"),
        (1, "star1"),
    )

    title: str | models.CharField = models.CharField(max_length=100)
    body: str | models.TextField = models.TextField()
    rating: int | models.IntegerField = models.IntegerField(
        choices=RATING_CHOICES, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    author: models.ForeignKey = models.ForeignKey(
        Customer,
        related_name="reviews",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    product: models.ForeignKey = models.ForeignKey(
        Product, related_name="reviews", on_delete=models.CASCADE
    )
    created_at: datetime | models.DateTimeField = models.DateTimeField(
        default=timezone.now
    )

    def __str__(self) -> str:
        return self.title
