from unittest.mock import patch

from django.urls import reverse
from django.test import TestCase
from django.http import HttpResponse


class CreateCheckoutSessionTests(TestCase):

    @patch("payments.views.StripePaymentProvider")
    def test_redirect_to_stripe(self, mock_provider):
        instance = mock_provider.return_value
        instance.create_checkout_session.return_value = "https://stripe.test/session"

        response = self.client.get(reverse("stripe-view", args=[1]))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "https://stripe.test/session")

    @patch("payments.views.StripePaymentProvider")
    def test_exception_when_session_missing(self, mock_provider):
        instance = mock_provider.return_value
        instance.create_checkout_session.return_value = None

        with self.assertRaises(Exception):
            self.client.get(reverse("stripe-view", args=[1]))


class StripeWebhookTests(TestCase):

    @patch("payments.views.StripePaymentProvider")
    def test_webhook_post(self, mock_provider):
        instance = mock_provider.return_value
        instance.handle_webhook.return_value = HttpResponse(status=200)

        response = self.client.post(reverse("stripe-webhook"))

        self.assertEqual(response.status_code, 200)

    def test_webhook_rejects_get(self):
        response = self.client.get(reverse("stripe-webhook"))

        self.assertEqual(response.status_code, 405)


class StripeSuccessViewTests(TestCase):

    def test_success_template(self):
        response = self.client.get(reverse("stripe-success-view"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "payments/success.html")


class StripeCancelViewTests(TestCase):

    def test_cancel_template(self):
        response = self.client.get(reverse("stripe-cancel-view"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "payments/cancel.html")
