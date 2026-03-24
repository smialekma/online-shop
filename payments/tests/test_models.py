from django.test import TestCase
from payments.factories import PaymentFactory


class PaymentModelTests(TestCase):
    def setUp(self):
        self.payment = PaymentFactory(is_paid=False)

    def test_get_status_unpaid(self):
        status = self.payment.get_status_for_display()

        self.assertEqual(status, "Unpaid")

    def test_get_status_paid(self):
        payment = PaymentFactory(is_paid=True)

        status = payment.get_status_for_display()

        self.assertEqual(status, "Paid")
