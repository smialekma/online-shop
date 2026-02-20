from datetime import timezone

import factory

from newsletter.models import Subscriber, NewsletterPost


class SubscriberFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Subscriber

    email = factory.LazyAttribute(lambda obj: f"{obj.username}@gmail.com")

    is_active = True
    date_subscribed = factory.Faker("date_time", tzinfo=timezone.utc)


class NewsletterPostFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = NewsletterPost

    title = factory.Faker("text", max_nb_chars=100)
    body = factory.Faker("text", max_nb_chars=500)
    created_at = factory.Faker("date_time", tzinfo=timezone.utc)
    is_published = False
    to_publish = False
