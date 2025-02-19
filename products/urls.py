from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.products, name="product-view"),
]