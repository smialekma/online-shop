from datetime import timezone

import factory

from customers.factories import CustomerFactory
from products.factories import ProductFactory
from wishlist.models import WishlistItem


class WishlistItemFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = WishlistItem

    product = factory.SubFactory(ProductFactory)
    customer = factory.SubFactory(CustomerFactory)
    date_added = factory.Faker("date_time", tzinfo=timezone.utc)
