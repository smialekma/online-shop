from django.db import models
from django.utils import timezone
from PIL import Image


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
    name = models.CharField(max_length=30)
    brand = models.CharField()
    description = models.TextField()
    photo = models.ImageField(upload_to="product_pics")
    price = models.IntegerField()
    quantity = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_added = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.photo.path)

        if img.height > 600 or img.width > 600:
            output_size = (600, 600)
            img.thumbnail(output_size)
            img.save(self.photo.path)

    def __str__(self):
        return self.name

