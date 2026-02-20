from unittest import TestCase

from customer_addresses.factories import CustomerAddressFactory
from customer_addresses.models import CustomerAddress


class TestCustomerAddressFactory(TestCase):
    def test_single_object_created(self) -> None:
        obj = CustomerAddressFactory.create()

        address = CustomerAddress.objects.get(pk=obj.pk)
        self.assertEqual(CustomerAddress.objects.count(), 1)
        self.assertIsNotNone(address.name)

    def test_multiple_object_created(self) -> None:
        CustomerAddressFactory.create(batch=5)
        self.assertEqual(CustomerAddress.objects.count(), 5)
