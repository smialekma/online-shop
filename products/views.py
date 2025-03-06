from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Product


class ProductView(ListView):
    model = Product
    template_name = "products/products.html"
    context_object_name = "products"
    ordering = ["date_added"]
    paginate_by = 9


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_details.html"
    context_object_name = "product"
