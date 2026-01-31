from django.urls import path

from carts.views import CartView, cart_update, RemoveFromCartView

urlpatterns = [
    path("cart/", CartView.as_view(), name="cart-view"),
    path("cart/update/", cart_update, name="cart-update"),
    path("cart/remove/", RemoveFromCartView.as_view(), name="cart-remove"),
]
