from django.urls import path
from .views import ProductView, ProductDetailView, add_product, remove_product

urlpatterns = [
    path("products/", ProductView.as_view(), name="product-view"),
    path("products/<int:pk>", ProductDetailView.as_view(), name="detail-view"),
    path("products/add", add_product, name="product-add"),
    path("products/remove", remove_product, name="product-remove"),
]
