from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Product
from django.shortcuts import redirect

from carts.cart import Cart


class ProductView(ListView):
    model = Product
    template_name = "products/products.html"
    context_object_name = "products"
    ordering = ["date_added"]
    paginate_by = 3


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_details.html"
    context_object_name = "product"


def add_product(request):
    product_id = request.POST.get('product_id')
    product = get_object_or_404(Product, id=product_id)

    cart = Cart(request)
    cart.add(product)

    return redirect('product-view')
