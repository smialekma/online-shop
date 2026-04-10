from django.test import TestCase

from newsletter.forms import NewsletterForm
from newsletter.models import Subscriber


class NewsletterFormTests(TestCase):

    def test_form_valid(self):
        form = NewsletterForm(data={"email": "test@example.com"})

        self.assertTrue(form.is_valid())

    def test_email_required(self):
        form = NewsletterForm(data={"email": ""})

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_invalid_email_format(self):
        form = NewsletterForm(data={"email": "invalid-email"})

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_form_save(self):
        form = NewsletterForm(data={"email": "test@example.com"})

        self.assertTrue(form.is_valid())

        subscriber = form.save()

        self.assertIsInstance(subscriber, Subscriber)
        self.assertEqual(subscriber.email, "test@example.com")

    def test_only_email_field_present(self):
        form = NewsletterForm()

        self.assertEqual(list(form.fields.keys()), ["email"])
