from django.urls import path
from .views import CheckoutView, CheckoutLoginView, OrderHistoryView, OrderDetailView

urlpatterns = [
    path("checkout/", CheckoutView.as_view(), name="checkout-view"),
    path("checkout/login", CheckoutLoginView.as_view(), name="checkout-login"),
    path("orders", OrderHistoryView.as_view(), name="order-history-view"),
    path("orders/<int:pk>", OrderDetailView.as_view(), name="order-detail-view"),
]
