from unittest import TestCase

from customers.factories import CustomerFactory
from customers.models import Customer


class TestCustomerFactory(TestCase):
    def test_single_object_created(self) -> None:
        obj = CustomerFactory.create()

        customer = Customer.objects.get(pk=obj.pk)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertIsNotNone(customer.name)

    def test_multiple_object_created(self) -> None:
        CustomerFactory.create(batch=5)
        self.assertEqual(Customer.objects.count(), 5)
