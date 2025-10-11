from datetime import timezone

import factory

from customers.factories import CustomerFactory
from product_reviews.models import Review
from products.factories import ProductFactory

RATING_CHOICES = (5, 4, 3, 2, 1)


class ReviewFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Review

    title = factory.Faker("text", max_nb_chars=100)
    body = factory.Faker("text", max_nb_chars=500)
    rating = factory.Iterator(RATING_CHOICES)
    author = factory.SubFactory(CustomerFactory)
    product = factory.SubFactory(ProductFactory)
    created_at = factory.Faker("date_time", tzinfo=timezone.utc)
