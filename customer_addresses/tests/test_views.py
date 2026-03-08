from django.test import TestCase
from django.urls import reverse, reverse_lazy
from django.contrib.messages import get_messages

from customer_addresses.factories import CustomerAddressFactory
from customer_addresses.models import CustomerAddress
from customers.factories import CustomerFactory


class EditAddressViewTests(TestCase):

    def setUp(self):
        self.user = CustomerFactory()
        self.url = reverse_lazy("edit-address-view")

    def test_login_required(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse_lazy("login-view"), response.url)

    def test_get_form_for_logged_user(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "customer_addresses/edit_address.html")

    def test_create_address_success(self):
        self.client.force_login(self.user)

        data = {
            "first_name": "John",
            "last_name": "Doe",
            "address_line": "Test Street 1",
            "telephone": "123 456 789",
            "city": "Warsaw",
            "postal_code": "00-001",
            "country": "Poland",
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("account-view"))

        self.assertTrue(
            CustomerAddress.objects.filter(
                user=self.user, street="Test Street 1"
            ).exists()
        )

    def test_success_message_added(self):
        self.client.force_login(self.user)

        data = {
            "first_name": "John",
            "last_name": "Doe",
            "address_line": "Test Street 1",
            "telephone": "123 456 789",
            "city": "Warsaw",
            "postal_code": "00-001",
            "country": "Poland",
        }

        response = self.client.post(self.url, data, follow=True)

        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(
            any("successfully saved" in str(message) for message in messages)
        )

    def test_initial_data_contains_user_data(self):
        self.client.force_login(self.user)

        address = CustomerAddressFactory.create(customer=self.user)

        response = self.client.get(self.url)

        form = response.context["form"]

        self.assertEqual(form.initial.get("address_line"), address.address_line)
        self.assertEqual(form.initial.get("last_name"), address.last_name)
