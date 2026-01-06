from django.urls import path
from .views import subscribe_newsletter, confirm_subscription

urlpatterns = [
    path("subscribe/", subscribe_newsletter, name="subscribe-newsletter"),
    path(
        "confirm-subscription/<uidb64>/<token>",
        confirm_subscription,
        name="confirm-subscription-view",
    ),
]
