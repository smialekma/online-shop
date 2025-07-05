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

    title = models.CharField(max_length=100)
    body = models.TextField()
    rating = models.IntegerField(
        choices=RATING_CHOICES, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
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
