import factory

from .models import Customer


class CustomerFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Customer

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@gmail.com")

    is_active = True
    is_staff = False
    is_superuser = False
    is_manager = False

    password = factory.PostGenerationMethodCall("set_password", "defaultpassword")