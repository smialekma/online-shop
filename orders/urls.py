from django.urls import path
from .views import CheckoutView, CheckoutLoginView

urlpatterns = [
    path("checkout/", CheckoutView.as_view(), name="checkout-view"),
    path("checkout/login", CheckoutLoginView.as_view(), name="checkout-login"),
]
