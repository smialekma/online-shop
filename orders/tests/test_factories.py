from django.test import TestCase

from dashboard.tests.test_dashboard_views import BaseTestClass
from orders.factories import ShippingMethodFactory, OrderFactory, OrderItemFactory
from orders.models import ShippingMethod, Order, OrderItem


class TestShippingMethodFactory(TestCase):
    def test_single_object_created(self) -> None:
        obj = ShippingMethodFactory.create()

        method = ShippingMethod.objects.get(pk=obj.pk)
        self.assertEqual(ShippingMethod.objects.count(), 1)
        self.assertIsNotNone(method.name)

    def test_multiple_object_created(self) -> None:
        ShippingMethodFactory.create_batch(5)
        self.assertEqual(ShippingMethod.objects.count(), 5)


class TestOrderFactory(BaseTestClass):
    def test_single_object_created(self) -> None:
        obj = OrderFactory.create()

        order = Order.objects.get(pk=obj.pk)
        self.assertEqual(Order.objects.count(), 1)
        self.assertIsNotNone(order.email)

    def test_multiple_object_created(self) -> None:
        OrderFactory.create_batch(5)
        self.assertEqual(Order.objects.count(), 5)


class TestOrderItemFactory(BaseTestClass):
    def test_single_object_created(self) -> None:
        obj = OrderItemFactory.create()

        item = OrderItem.objects.get(pk=obj.pk)
        self.assertEqual(OrderItem.objects.count(), 1)
        self.assertIsNotNone(item.product.name)

    def test_multiple_object_created(self) -> None:
        OrderItemFactory.create_batch(5)
        self.assertEqual(OrderItem.objects.count(), 5)
