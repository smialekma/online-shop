import json

from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView, View

from carts.cart import Cart
from products.models import Product


class CartView(TemplateView):
    template_name = "carts/cart.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        cart_items = list(cart)

        paginator = Paginator(cart_items, 3)
        page_number = self.request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)
        print(f"Total pages: {paginator.num_pages}")
        context_data["page_obj"] = page_obj
        context_data["paginator"] = paginator
        context_data["products"] = page_obj

        return context_data


@require_POST
def cart_update(request: HttpRequest) -> JsonResponse:
    data = json.loads(request.body)
    product_id = str(data.get("product_id"))
    requested_qty = int(data.get("quantity", 0))

    cart = Cart(request)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)

    max_stock = product.quantity

    # stock limit
    if requested_qty > max_stock:
        cart.upsert(product, max_stock, True)
        return JsonResponse(
            {
                "limited": True,
                "quantity": max_stock,
                "message": "Not enough stock available",
            }
        )

    # update
    cart.upsert(product, requested_qty, True)

    cart_html = render_to_string(
        "partials/cart_items.html", {"cart": cart}, request=request
    )

    return JsonResponse(
        {
            "success": True,
            "quantity": requested_qty,
            "cart_count": len(cart),
            "cart_html": cart_html,
            "cart_total": str(cart.get_total_price()),
        }
    )


class RemoveFromCartView(View):
    def post(self, request: HttpRequest) -> HttpResponseRedirect:
        product_id = request.POST.get("product_id")

        cart = Cart(request)

        cart.remove(product_id)
        messages.success(request, "Product was removed from your cart.")

        return self._redirect_back(request)

    def _redirect_back(self, request: HttpRequest) -> HttpResponseRedirect:
        return redirect(request.META.get("HTTP_REFERER", "/"))
