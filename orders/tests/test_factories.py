from unittest import TestCase

from orders.factories import ShippingMethodFactory, OrderFactory, OrderItemFactory
from orders.models import ShippingMethod, Order, OrderItem


class TestShippingMethodFactory(TestCase):
    def test_single_object_created(self) -> None:
        obj = ShippingMethodFactory.create()

        method = ShippingMethod.objects.get(pk=obj.pk)
        self.assertEqual(ShippingMethod.objects.count(), 1)
        self.assertIsNotNone(method.name)

    def test_multiple_object_created(self) -> None:
        ShippingMethodFactory.create(batch=5)
        self.assertEqual(ShippingMethod.objects.count(), 5)


class TestOrderFactory(TestCase):
    def test_single_object_created(self) -> None:
        obj = OrderFactory.create()

        order = Order.objects.get(pk=obj.pk)
        self.assertEqual(Order.objects.count(), 1)
        self.assertIsNotNone(order.name)

    def test_multiple_object_created(self) -> None:
        OrderFactory.create(batch=5)
        self.assertEqual(Order.objects.count(), 5)


class TestOrderItemFactory(TestCase):
    def test_single_object_created(self) -> None:
        obj = OrderItemFactory.create()

        item = OrderItem.objects.get(pk=obj.pk)
        self.assertEqual(OrderItem.objects.count(), 1)
        self.assertIsNotNone(item.name)

    def test_multiple_object_created(self) -> None:
        OrderItemFactory.create(batch=5)
        self.assertEqual(OrderItem.objects.count(), 5)
