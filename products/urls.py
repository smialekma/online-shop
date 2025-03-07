from django.contrib import admin
from django.urls import path
from .views import ProductView, ProductDetailView

urlpatterns = [
    path('products/', ProductView.as_view(), name="product-view"),
    path('products/<int:pk>', ProductDetailView.as_view(), name="detail-view")
]