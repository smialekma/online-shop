import factory

from .models import Customer
from customer_addresses.factories import CustomerAddressFactory


class CustomerFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Customer

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@gmail.com")

    is_active = True
    is_staff = False
    is_superuser = False

    password = factory.PostGenerationMethodCall("set_password", "defaultpassword")
    address = factory.SubFactory(CustomerAddressFactory)
