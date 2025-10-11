import factory

from .models import CustomerAddress


class CustomerAddressFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = CustomerAddress

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    address_line = factory.Faker("street_address")

    telephone = factory.Faker("phone_number")
    city = factory.Faker("city")
    postal_code = factory.Faker("postcode")
    country = factory.Faker("country")
