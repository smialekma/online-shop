import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class SubscriberTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, subscriber, timestamp):
        return (
            six.text_type(subscriber.pk)
            + six.text_type(timestamp)
            + six.text_type(subscriber.is_active)
        )


newsletter_activation_token = SubscriberTokenGenerator()
