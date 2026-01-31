from django.contrib import messages
from django.db.models import Count, Prefetch, Avg, QuerySet
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.template.loader import render_to_string
from product_reviews.models import Review
from .filters import ProductFilter
from .models import Product, ProductImage
from django.shortcuts import redirect
from product_reviews.forms import ReviewForm
from django.core.serializers.json import DjangoJSONEncoder

from carts.cart import Cart
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from typing import Optional, Any


class ProductView(ListView):
    model = Product
    template_name = "products/products.html"
    # filterset_class = ProductFilter
    # context_object_name = "filter"
    ordering = ["date_added"]
    # paginate_by = 3

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context_data = super().get_context_data(**kwargs)

        f = ProductFilter(
            self.request.GET,
            queryset=Product.objects.all()
            .prefetch_related("reviews")
            .annotate(average_rating=Avg("reviews__rating")),
        )

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
                    .annotate(count=Count("order_items"))
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


class ProductDetailView(CreateView, DetailView):
    model = Product
    template_name = "products/product_details.html"
    form_class = ReviewForm

    def get_context_data(
        self, *, object_list: Optional[QuerySet[Product]] = None, **kwargs: Any
    ) -> dict[str, Any]:
        context_data = super().get_context_data(**kwargs)

        product = self.get_object()
        context_data["product"] = product
        reviews = (
            Review.objects.filter(product_id=product.id)
            .select_related("author")
            .order_by("-created_at")
        )

        paginator = Paginator(reviews, 3)
        page_number = self.request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)
        context_data["page_obj"] = page_obj
        context_data["paginator"] = paginator

        review_aggregations = reviews.aggregate(
            average_rating=Avg("rating"), review_count=Count("id")
        )
        context_data["review_aggregations"] = review_aggregations
        context_data["reviews"] = page_obj
        context_data["rating_options"] = (1, 2, 3, 4, 5)

        context_data["related_products"] = product.get_related_products(limit=5)
        context_data["form"] = ReviewForm()
        return context_data

    def form_valid(self, form: ReviewForm) -> HttpResponse:
        obj = form.save(commit=False)
        obj.author = self.request.user
        product = self.get_object()
        obj.product = product
        obj.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return str(self.get_object().id)


def add_to_cart(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        product = get_object_or_404(Product, id=product_id)

        cart = Cart(request)
        cart.upsert(product)

        cart_html = render_to_string(
            "partials/cart_items.html", {"cart": cart}, request=request
        )

        return JsonResponse(
            {
                "success": True,
                "message": "Product added to cart",
                "cart_count": len(cart),
                "cart_html": cart_html,
                "cart_total": str(cart.get_total_price()),
            },
            encoder=DjangoJSONEncoder,
        )

    return JsonResponse({"success": False}, status=400)


@require_POST
def add_to_cart_with_qty(request, pk):
    product_id = pk
    quantity = int(request.POST.get("quantity", 1))

    product = get_object_or_404(Product, id=product_id)

    cart = Cart(request)

    qty_in_cart = 0
    if cart.get_item(product_id) is not None:
        qty_in_cart = cart.get_item(product_id).get("quantity")

    available_quantity = product.quantity - qty_in_cart

    if available_quantity <= 0:
        messages.warning(request, "Product out of stock!")
    elif available_quantity < quantity:
        cart.upsert(product, available_quantity, False)
        messages.info(
            request,
            f"Product out of stock. Only {str(available_quantity)} items added to cart.",
        )
    else:
        cart.upsert(product, quantity, False)
        messages.success(request, "Items added to cart.")

    return redirect(request.META.get("HTTP_REFERER", "/"))


#
# def remove_from_cart(request: HttpRequest) -> HttpResponseRedirect:
#     product_id = request.POST.get("product_id")
#     product = get_object_or_404(Product, id=product_id)
#     # print(product.id)
#
#     cart = Cart(request)
#     cart.remove(product)
#
#     return redirect("product-view")


def remove_from_cart(request: HttpRequest) -> JsonResponse | HttpResponseRedirect:
    if request.method == "POST":
        product_id = request.POST.get("product_id")

        cart = Cart(request)
        cart.remove(product_id)

        cart_html = render_to_string(
            "partials/cart_items.html", {"cart": cart}, request=request
        )
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse(
                {
                    "success": True,
                    "message": "Product removed from cart",
                    "cart_count": len(cart),
                    "cart_html": cart_html,
                    "cart_total": str(cart.get_total_price()),
                }
            )
        return redirect(request.META.get("HTTP_REFERER", "/"))
    return redirect(request.META.get("HTTP_REFERER", "/"))
