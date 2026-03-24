from django.test import TestCase

from customer_addresses.forms import AddressForm, CheckoutForm
from customer_addresses.models import CustomerAddress
from orders.factories import ShippingMethodFactory


class AddressFormTests(TestCase):

    def setUp(self):
        self.valid_data = {
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "address_line": "Test Street 1",
            "telephone": "123456789",
            "postal_code": "00-001",
            "city": "Warsaw",
            "country": "PL",
        }

    def test_address_form_valid(self):
        form = AddressForm(data=self.valid_data)

        self.assertTrue(form.is_valid())

    def test_address_form_invalid_without_email(self):
        data = self.valid_data.copy()
        data.pop("email")

        form = AddressForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_address_created(self):
        form = AddressForm(data=self.valid_data)

        self.assertTrue(form.is_valid())

        address = form.save()

        self.assertIsInstance(address, CustomerAddress)
        self.assertEqual(address.address_line, "Test Street 1")


class CheckoutFormTests(TestCase):

    def setUp(self):
        self.shipping = ShippingMethodFactory()

        self.valid_data = {
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "address_line": "Test Street 1",
            "telephone": "123456789",
            "postal_code": "00-001",
            "city": "Warsaw",
            "country": "PL",
            "order_notes": "Leave at door",
            "agree": True,
            "shipping_method": self.shipping.id,
        }

    def test_checkout_form_valid(self):
        form = CheckoutForm(data=self.valid_data)

        self.assertTrue(form.is_valid())

    def test_checkout_form_requires_agree(self):
        data = self.valid_data.copy()
        data["agree"] = False

        form = CheckoutForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("agree", form.errors)

    def test_shipping_method_required(self):
        data = self.valid_data.copy()
        data.pop("shipping_method")

        form = CheckoutForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("shipping_method", form.errors)

    def test_shipping_method_label_from_instance(self):
        form = CheckoutForm()

        field = form.fields["shipping_method"]

        label = field.label_from_instance(self.shipping)

        self.assertEqual(label, self.shipping)
