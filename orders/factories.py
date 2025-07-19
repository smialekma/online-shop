from datetime import timedelta, timezone

import factory
from factory import LazyAttribute

from customer_addresses.factories import CustomerAddressFactory
from customers.factories import CustomerFactory
from orders.models import Order, OrderItem
from products.factories import ProductFactory


class OrderFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Order

    customer = factory.SubFactory(CustomerFactory)
    is_payed = True
    date_ordered = LazyAttribute(
        lambda obj: obj.created_at
        + timedelta(
            minutes=factory.Faker("random_int", min=1, max=1440).evaluate(
                obj, None, extra={"locale": "en_US"}
            )
        )
    )
    date_fulfilled = LazyAttribute(
        lambda obj: obj.updated_at
        + timedelta(
            minutes=factory.Faker("random_int", min=1, max=1440).evaluate(
                obj, None, extra={"locale": "en_US"}
            )
        )
    )
    address = factory.SubFactory(CustomerAddressFactory)
    created_at = factory.Faker(
        "date_time_between", start_date="-30d", end_date="-3d", tzinfo=timezone.utc
    )
    updated_at = LazyAttribute(
        lambda obj: obj.date_ordered
        + timedelta(
            minutes=factory.Faker("random_int", min=1, max=1440).evaluate(
                obj, None, extra={"locale": "en_US"}
            )
        )
    )
    total_amount = factory.Faker(
        "pydecimal", left_digits=4, right_digits=2, positive=True
    )


class OrderItemFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
