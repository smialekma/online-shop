from django.urls import path
from .views import (
    ProductView,
    ProductDetailView,
    add_to_cart,
    remove_from_cart,
    add_to_cart_with_qty,
)

urlpatterns = [
    path("products/", ProductView.as_view(), name="product-view"),
    path("products/<int:pk>", ProductDetailView.as_view(), name="detail-view"),
    path("products/<int:pk>/add", add_to_cart_with_qty, name="detail-add"),
    path("products/add", add_to_cart, name="product-add"),
    path("products/remove", remove_from_cart, name="product-remove"),
]
