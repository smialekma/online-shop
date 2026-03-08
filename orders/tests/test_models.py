from decimal import Decimal

from django.test import TestCase

from orders.factories import ShippingMethodFactory, OrderFactory, OrderItemFactory
from payments.factories import PaymentFactory
from products.factories import ProductFactory


class ShippingMethodModelTests(TestCase):

    def test_str_returns_name(self):
        method = ShippingMethodFactory(name="Courier")

        self.assertEqual(str(method), "Courier")

    def test_delivery_time_same_days(self):
        method = ShippingMethodFactory(
            min_delivery_time_in_days=2, max_delivery_time_in_days=2
        )

        self.assertEqual(method.get_delivery_time_for_display(), "2 day(s)")

    def test_delivery_time_range(self):
        method = ShippingMethodFactory(
            min_delivery_time_in_days=2, max_delivery_time_in_days=5
        )

        self.assertEqual(method.get_delivery_time_for_display(), "2 - 5 days")


class OrderModelTests(TestCase):

    def setUp(self):
        self.order = OrderFactory(total_amount=100)

    def test_is_paid_false_without_payment(self):
        self.assertFalse(self.order.is_paid)

    def test_is_paid_false_when_payment_not_paid(self):
        PaymentFactory(order=self.order, is_paid=False)

        self.assertFalse(self.order.is_paid)

    def test_is_paid_true_when_paid_payment_exists(self):
        PaymentFactory(order=self.order, is_paid=True)

        self.assertTrue(self.order.is_paid)

    def test_get_status_unpaid(self):
        status = self.order.get_status_for_display()

        self.assertEqual(status, "Unpaid")

    def test_get_status_paid(self):
        PaymentFactory(order=self.order, is_paid=True)

        status = self.order.get_status_for_display()

        self.assertEqual(status, "Paid")


class OrderItemModelTests(TestCase):

    def test_get_subtotal(self):
        product = ProductFactory(price=Decimal("10.00"))

        order = OrderFactory(total_amount=10)

        item = OrderItemFactory(order=order, product=product, quantity=3)

        self.assertEqual(item.get_subtotal(), Decimal("30.00"))
