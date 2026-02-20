from datetime import datetime

from django.db import models


class Subscriber(models.Model):
    email: str | models.EmailField = models.EmailField(
        unique=True, blank=False, null=False
    )
    is_active: bool | models.BooleanField = models.BooleanField(default=False)
    date_subscribed: datetime | models.DateTimeField = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self) -> str:
        return self.email


class NewsletterPost(models.Model):
    title: str | models.CharField = models.CharField(max_length=100)
    body: str | models.CharField = models.TextField()
    created_at: datetime | models.DateTimeField = models.DateTimeField(
        auto_now_add=True
    )
    is_published: bool | models.BooleanField = models.BooleanField(default=False)
    to_publish: bool | models.BooleanField = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title
