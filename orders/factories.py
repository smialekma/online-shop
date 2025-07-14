import factory

from customer_addresses.factories import CustomerAddressFactory
from customers.factories import CustomerFactory
from orders.models import Order, OrderItem
from products.factories import ProductFactory


class OrderFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Order

    customer = factory.SubFactory(CustomerFactory)
    is_payed = True
    date_ordered = factory.Faker("date_time")
    date_fulfilled = factory.Faker("date_time")
    address = factory.SubFactory(CustomerAddressFactory)
    created_at = factory.Faker("date_time")
    updated_at = factory.Faker("date_time")
    total_amount = factory.Faker(
        "pydecimal", left_digits=4, right_digits=2, positive=True
    )


class OrderItemFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
