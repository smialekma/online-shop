from _pydatetime import datetime
from decimal import Decimal

from django.db import models
from PIL import Image
from django.db.models import Count, Avg
from django.utils import timezone
from typing import Any

from orders.models import OrderItem


class Brand(models.Model):
    name: str | models.CharField = models.CharField()

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name: str | models.CharField = models.CharField()
    photo = models.ImageField(upload_to="category_pics")  # type: ignore

    def save(self, *args: Any, **kwargs: Any) -> None:
        super().save(*args, **kwargs)

        img = Image.open(self.photo.path)

        if img.height > 400 or img.width > 600:
            output_size = (400, 600)
            img.thumbnail(output_size)
            img.save(self.photo.path)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name: str | models.CharField = models.CharField(
        max_length=30, help_text="name of the product"
    )
    brand: models.ForeignKey = models.ForeignKey(
        Brand, related_name="products", on_delete=models.CASCADE
    )
    description: str | models.TextField = models.TextField()
    details: str | models.TextField = models.TextField()
    price: float | Decimal | models.DecimalField = models.DecimalField(
        decimal_places=2, max_digits=8
    )
    quantity: int | models.IntegerField = models.IntegerField()
    category: models.ForeignKey = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )
    date_added: datetime | models.DateTimeField = models.DateTimeField(
        default=timezone.now
    )

    is_sale: bool | models.BooleanField = models.BooleanField(default=False)
    old_price: float | Decimal | models.DecimalField = models.DecimalField(
        decimal_places=2, max_digits=8, null=True, blank=True
    )

    def __str__(self) -> str:
        return self.name

    def is_new(self) -> bool:
        return (timezone.now() - self.date_added).days < 10

    def sale_percentage(self) -> int:
        return abs(
            round(
                (float(self.old_price) - float(self.price))
                / float(self.old_price)
                * 100
            )
        )

    def get_related_products(self, *, limit: int) -> list[dict[str, Any]]:
        order_ids = OrderItem.objects.filter(product_id=self).values_list(
            "order_id", flat=True
        )

        related_products_ids = (
            OrderItem.objects.filter(order_id__in=order_ids)
            .exclude(product_id=self)
            .values_list("product_id", flat=True)
        )

        products_counts = (
            OrderItem.objects.filter(product_id__in=related_products_ids)
            .values("product_id")
            .annotate(count=Count("product_id"))
            .order_by("-count")
        )

        related_products = []

        for item in products_counts[:limit]:
            product = (
                Product.objects.filter(id=item["product_id"])
                .prefetch_related("reviews")
                .annotate(average_rating=Avg("reviews__rating"))
            )[0]
            main_photo = ProductImage.objects.filter(
                product_id=product, is_main_photo=True
            ).first()

            related_products.append({"product": product, "main_photo": main_photo})
        return related_products


class ProductImage(models.Model):
    photo = models.ImageField(upload_to="product_pics")  # type: ignore
    is_main_photo: bool | models.BooleanField = models.BooleanField(default=False)
    product: models.ForeignKey = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE
    )

    def save(self, *args: Any, **kwargs: Any) -> None:
        super().save(*args, **kwargs)

        img = Image.open(self.photo.path)

        if img.height > 600 or img.width > 600:
            output_size = (600, 600)
            img.thumbnail(output_size)
            img.save(self.photo.path)
