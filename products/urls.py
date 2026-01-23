from django.urls import path
from .views import ProductView, ProductDetailView, add_to_cart1, remove_from_cart

urlpatterns = [
    path("products/", ProductView.as_view(), name="product-view"),
    path("products/<int:pk>", ProductDetailView.as_view(), name="detail-view"),
    path("products/add", add_to_cart1, name="product-add"),
    path("products/remove", remove_from_cart, name="product-remove"),
]
