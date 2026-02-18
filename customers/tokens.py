import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from customers.models import Customer


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: Customer, timestamp) -> str:
        return (
            six.text_type(user.pk)
            + six.text_type(timestamp)
            + six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()
