from datetime import timezone

from django.db import models
from PIL import Image


class Brand(models.Model):
    name = models.CharField()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField()
    photo = models.ImageField(upload_to="category_pics")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.photo.path)

        if img.height > 400 or img.width > 600:
            output_size = (400, 600)
            img.thumbnail(output_size)
            img.save(self.photo.path)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=30, help_text="name of the product")
    brand = models.ForeignKey(Brand, related_name="products", on_delete=models.CASCADE)
    description = models.TextField()
    details = models.TextField()
    price = models.IntegerField()
    quantity = models.IntegerField()
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )
    date_added = models.DateTimeField(default=timezone.now)

    is_sale = models.BooleanField(default=False)
    old_price = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    def newer_than_x_days(self) -> bool:
        return (timezone.now() - self.date_added).days < 10

    def sale_percentage(self) -> int:
        return round((self.old_price - self.price) / self.old_price * 100)


class ProductImage(models.Model):
    photo = models.ImageField(upload_to="product_pics")
    is_main_photo = models.BooleanField(default=False)
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.photo.path)

        if img.height > 600 or img.width > 600:
            output_size = (600, 600)
            img.thumbnail(output_size)
            img.save(self.photo.path)
