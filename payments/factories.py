from datetime import timezone

import factory

from orders.factories import OrderFactory
from payments.models import Payment


class PaymentFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Payment

    stripe_checkout_id = factory.Faker("text", max_nb_chars=20)
    order = factory.SubFactory(OrderFactory)
    is_paid = True
    amount = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    payment_method = factory.Iterator(["card", "blik", "wire transfer"])
    created_at = factory.Faker("date_time", tzinfo=timezone.utc)
