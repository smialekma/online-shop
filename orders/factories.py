from datetime import timedelta, timezone

import factory
from factory import LazyAttribute

from customer_addresses.factories import CustomerAddressFactory
from orders.models import Order, OrderItem, ShippingMethod
from products.factories import ProductFactory


class ShippingMethodFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = ShippingMethod

    name = factory.Sequence(lambda n: f"method{n}")
    price = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
    min_delivery_time_in_days = factory.Faker("random_int", min=1, max=5)
    max_delivery_time_in_days = LazyAttribute(
        lambda obj: obj.min_delivery_time_in_days
        + factory.Faker("random_int", min=1, max=3).evaluate(
            obj, None, extra={"locale": "en_US"}
        )
    )


class OrderFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Order

    customer = factory.SubFactory("customers.factories.CustomerFactory")
    created_at = factory.Faker(
        "date_time_between", start_date="-30d", end_date="-3d", tzinfo=timezone.utc
    )
    date_ordered = LazyAttribute(
        lambda obj: obj.created_at
        + timedelta(
            minutes=factory.Faker("random_int", min=1, max=1440).evaluate(
                obj, None, extra={"locale": "en_US"}
            )
        )
    )
    updated_at = LazyAttribute(
        lambda obj: obj.date_ordered
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

    total_amount = factory.Faker(
        "pydecimal", left_digits=4, right_digits=2, positive=True
    )

    order_notes = factory.Faker("text", max_nb_chars=200)

    email = factory.LazyAttribute(lambda obj: obj.customer.email)
    shipping_method = factory.SubFactory(ShippingMethodFactory)


class OrderItemFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = factory.Faker("random_int", min=1, max=5)
