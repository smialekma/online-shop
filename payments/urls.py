from django.urls import path
from .views import create_checkout_session, success, cancel, stripe_webhook

urlpatterns = [
    path(
        "create-checkout-session/<int:order_id>",
        create_checkout_session,
        name="stripe-view",
    ),
    path("payment/success", success, name="stripe-success-view"),
    path("payment/cancel", cancel, name="stripe-cancel-view"),
    path("payment/webhook", stripe_webhook, name="stripe-webhook"),
]
