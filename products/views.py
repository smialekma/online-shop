from django.db.models import Count, Prefetch
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .filters import ProductFilter
from .models import Product, ProductImage
from django.shortcuts import redirect

from carts.cart import Cart
from django.core.paginator import Paginator


class ProductView(ListView):
    model = Product
    template_name = "products/products.html"
    # filterset_class = ProductFilter
    # context_object_name = "filter"
    ordering = ["date_added"]
    # paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)

        f = ProductFilter(self.request.GET, queryset=Product.objects.all())
        context_data["filter"] = f

        paginator = Paginator(f.qs, 3)
        page_number = self.request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)
        context_data["page_obj"] = page_obj
        context_data["paginator"] = paginator
        context_data["products"] = page_obj

        context_data["top_selling_products"] = (
            (
                (
                    Product.objects.all()
                    .select_related("category")
                    .annotate(count=Count("orders"))
                ).order_by("-count")
            ).prefetch_related(
                Prefetch(
                    "images",
                    queryset=ProductImage.objects.filter(is_main_photo=True),
                    to_attr="main_images",
                )
            )
        )[:3]

        return context_data


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_details.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)

        product = self.get_object()
        context_data["product"] = product

        context_data["related_products"] = product.get_related_products(limit=5)
        print(context_data)
        return context_data


def add_product(request):
    product_id = request.POST.get("product_id")
    product = get_object_or_404(Product, id=product_id)

    cart = Cart(request)
    cart.add(product)

    return redirect("product-view")


def remove_product(request):
    product_id = request.POST.get("product_id")
    product = get_object_or_404(Product, id=product_id)
    print(product.id)

    cart = Cart(request)
    cart.remove(product)

    return redirect("product-view")
