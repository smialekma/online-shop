from unittest import TestCase

from payments.factories import PaymentFactory
from payments.models import Payment


class TestPaymentFactory(TestCase):
    def test_single_object_created(self) -> None:
        obj = PaymentFactory.create()

        payment = Payment.objects.get(pk=obj.pk)
        self.assertEqual(Payment.objects.count(), 1)
        self.assertIsNotNone(payment.name)

    def test_multiple_object_created(self) -> None:
        PaymentFactory.create(batch=5)
        self.assertEqual(Payment.objects.count(), 5)
