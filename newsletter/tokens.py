import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from newsletter.models import Subscriber


class SubscriberTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, subscriber: Subscriber, timestamp) -> str:
        return (
            six.text_type(subscriber.pk)
            + six.text_type(timestamp)
            + six.text_type(subscriber.is_active)
        )


newsletter_activation_token = SubscriberTokenGenerator()
