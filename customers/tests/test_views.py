from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from django.core import mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from customers.factories import CustomerFactory
from customers.models import Customer
from customers.tokens import account_activation_token


class RegisterViewTests(TestCase):

    def setUp(self):
        self.url = reverse("register-view")

    def test_register_creates_customer(self):
        data = {
            "username": "user123",
            "email": "test@example.com",
            "password1": "StrongPassword123!",
            "password2": "StrongPassword123!",
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Customer.objects.filter(email="test@example.com").exists())

    def test_register_sends_activation_email(self):
        data = {
            "username": "user123",
            "email": "test1@example.com",
            "password1": "StrongPassword123!",
            "password2": "StrongPassword123!",
        }

        self.client.post(self.url, data)

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("activate your account", mail.outbox[0].subject)

    def test_register_redirects_after_success(self):
        data = {
            "username": "user123",
            "email": "test2@example.com",
            "password1": "StrongPassword123!",
            "password2": "StrongPassword123!",
        }

        response = self.client.post(self.url, data)

        self.assertRedirects(response, reverse("home-view"))


class CustomLoginViewTests(TestCase):

    def setUp(self):
        self.customer = CustomerFactory.create()
        self.customer.set_password("testpass123")
        self.customer.save()

        self.url = reverse("login-view")

    def test_login_success(self):
        response = self.client.post(
            self.url,
            {"username": self.customer.email, "password": "testpass123"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue("_auth_user_id" in self.client.session)

    def test_success_message_added(self):
        response = self.client.post(
            self.url,
            {"username": self.customer.email, "password": "testpass123"},
        )

        messages = [m.message for m in get_messages(response.wsgi_request)]

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You have been successfully logged in.")


class CustomLogoutViewTests(TestCase):

    def setUp(self):
        self.customer = CustomerFactory()

        self.url = reverse("logout-view")

    def test_logout(self):
        self.client.force_login(self.customer)
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertFalse("_auth_user_id" in self.client.session)

    def test_success_message_added(self):
        self.client.force_login(self.customer)

        response = self.client.post(self.url)

        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(
            any(
                "You have been successfully logged out" in str(message)
                for message in messages
            )
        )


class ResetPasswordViewTests(TestCase):

    def setUp(self):
        self.customer = CustomerFactory(email="reset@example.com")
        self.url = reverse("password_reset")

    def test_password_reset_sends_email(self):
        response = self.client.post(self.url, {"email": self.customer.email})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)

    def test_password_reset_redirect(self):
        response = self.client.post(self.url, {"email": self.customer.email})

        self.assertRedirects(response, reverse("home-view"))


class PasswordResetConfirmViewTests(TestCase):

    def setUp(self):
        self.customer = CustomerFactory()
        self.customer.set_password("OldPassword123!")
        self.customer.save()

        uid = urlsafe_base64_encode(force_bytes(self.customer.pk))
        token = default_token_generator.make_token(self.customer)

        self.url = reverse(
            "password_reset_confirm",
            kwargs={"uidb64": uid, "token": token},
        )

    def test_password_reset_confirm(self):
        # 1. validate token
        self.client.get(self.url)

        # 2. submit new password
        response = self.client.post(
            self.url,
            {
                "new_password1": "NewStrongPassword123!",
                "new_password2": "NewStrongPassword123!",
            },
        )

        self.assertEqual(response.status_code, 302)


class ActivateAccountViewTests(TestCase):

    def setUp(self):
        self.customer = CustomerFactory(is_active=False)

        uid = urlsafe_base64_encode(force_bytes(self.customer.pk))
        token = account_activation_token.make_token(self.customer)

        self.valid_url = reverse(
            "activate-view",
            kwargs={"uidb64": uid, "token": token},
        )

        self.invalid_url = reverse(
            "activate-view",
            kwargs={"uidb64": uid, "token": "invalid-token"},
        )

    def test_activate_valid_token(self):
        response = self.client.get(self.valid_url)

        self.customer.refresh_from_db()

        self.assertTrue(self.customer.is_active)
        self.assertRedirects(response, reverse("login-view"))

    def test_activate_invalid_token(self):
        response = self.client.get(self.invalid_url)

        self.customer.refresh_from_db()

        self.assertFalse(self.customer.is_active)
        self.assertRedirects(response, reverse("login-view"))
