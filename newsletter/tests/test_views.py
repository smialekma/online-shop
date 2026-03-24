from django.contrib.messages import get_messages
from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from newsletter.factories import SubscriberFactory
from newsletter.models import Subscriber
from newsletter.tokens import newsletter_activation_token


class SubscribeNewsletterTests(TestCase):

    def setUp(self):
        self.url = reverse("subscribe-newsletter")

    def test_subscribe_valid_email(self):
        response = self.client.post(
            self.url,
            {"email": "test@example.com"},
            HTTP_REFERER="/",
            follow=True,
        )

        self.assertEqual(response.status_code, 200)

        self.assertTrue(Subscriber.objects.filter(email="test@example.com").exists())

        self.assertEqual(len(mail.outbox), 1)

    def test_success_message_added(self):
        response = self.client.post(
            self.url,
            {"email": "test@example.com"},
            HTTP_REFERER="/",
            follow=True,
        )

        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(any("successfully subscribed" in str(m) for m in messages))

    def test_invalid_form(self):
        response = self.client.post(
            self.url,
            {"email": ""},
            HTTP_REFERER="/",
            follow=True,
        )

        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(len(messages) > 0)


class SendEmailTests(TestCase):

    def test_activation_email_sent(self):
        subscriber = SubscriberFactory(email="mail@test.com")

        from newsletter.views import _send_email
        from django.contrib.sites.requests import RequestSite
        from django.test import RequestFactory

        request = RequestFactory().get("/")
        site = RequestSite(request)

        _send_email(site, subscriber, subscriber.email)

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("activate your newsletter subscription", mail.outbox[0].subject)


class ConfirmSubscriptionTests(TestCase):

    def setUp(self):
        self.subscriber = SubscriberFactory(is_active=False)

        uid = urlsafe_base64_encode(force_bytes(self.subscriber.pk))
        token = newsletter_activation_token.make_token(self.subscriber)

        self.valid_url = reverse(
            "confirm-subscription-view",
            kwargs={"uidb64": uid, "token": token},
        )

        self.invalid_url = reverse(
            "confirm-subscription-view",
            kwargs={"uidb64": uid, "token": "invalid-token"},
        )

    def test_confirm_subscription_valid(self):
        response = self.client.get(self.valid_url)

        self.subscriber.refresh_from_db()

        self.assertTrue(self.subscriber.is_active)
        self.assertEqual(response.status_code, 302)

    def test_confirm_subscription_invalid_token(self):
        response = self.client.get(self.invalid_url)

        self.subscriber.refresh_from_db()

        self.assertFalse(self.subscriber.is_active)
        self.assertEqual(response.status_code, 302)
