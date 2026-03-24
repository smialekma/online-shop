from django.db import models
from django.utils import timezone

from customers.models import Customer
from products.models import Product


class WishlistItem(models.Model):
    customer = models.ForeignKey(
        Customer, related_name="wishlist_items", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, related_name="wishlist_items", on_delete=models.CASCADE
    )
    date_added = models.DateTimeField(default=timezone.now)
