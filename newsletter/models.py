from django.db import models


class Subscriber(models.Model):
    email = models.EmailField(unique=True, blank=False, null=False)
    is_active = models.BooleanField(default=False)
    date_subscribed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class NewsletterPost(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    to_publish = models.BooleanField(default=False)

    def __str__(self):
        return self.title
