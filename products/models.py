from django.db import models
from django.utils import timezone
from PIL import Image


class Product(models.Model):
    name = models.CharField()
    description = models.TextField()
    photo = models.ImageField()
    price = models.IntegerField()
    quantity = models.IntegerField()
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
