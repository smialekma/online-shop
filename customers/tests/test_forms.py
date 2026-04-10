from django.test import TestCase

from customers.forms import CustomerRegisterForm
from customers.models import Customer


class CustomerRegisterFormTests(TestCase):

    def setUp(self):
        self.valid_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "StrongPassword123!",
            "password2": "StrongPassword123!",
        }

    def test_form_valid(self):
        form = CustomerRegisterForm(data=self.valid_data)

        self.assertTrue(form.is_valid())

    def test_user_created(self):
        form = CustomerRegisterForm(data=self.valid_data)

        self.assertTrue(form.is_valid())

        user = form.save()

        self.assertIsInstance(user, Customer)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")

    def test_password_mismatch(self):
        data = self.valid_data.copy()
        data["password2"] = "DifferentPassword123!"

        form = CustomerRegisterForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_email_required(self):
        data = self.valid_data.copy()
        data["email"] = ""

        form = CustomerRegisterForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
