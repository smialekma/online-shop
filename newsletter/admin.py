from django.contrib import admin

from newsletter.models import Subscriber, NewsletterPost

admin.site.register(Subscriber)
admin.site.register(NewsletterPost)
