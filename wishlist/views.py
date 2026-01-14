from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView

from products.models import Product
from wishlist.models import WishlistItem


class WishlistView(LoginRequiredMixin, ListView):
    template_name = "wishlist/wishlist.html"
    model = WishlistItem
    context_object_name = "items"
    ordering = "-date_added"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.is_authenticated:
            return (
                queryset.select_related("product")
                .prefetch_related("product__reviews")
                .filter(customer=self.request.user)
                .annotate(average_rating=Avg("product__reviews__rating"))
            )
        else:
            return []


@login_required
def add_to_wishlist(request: HttpRequest) -> HttpResponseRedirect:
    product_id = request.POST.get("product_id")
    product = get_object_or_404(Product, id=product_id)

    WishlistItem.objects.get_or_create(product=product, customer=request.user)

    return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def remove_from_wishlist(request: HttpRequest) -> HttpResponseRedirect:
    product_id = request.POST.get("product_id")
    product = get_object_or_404(Product, id=product_id)

    wishlist_item = get_object_or_404(
        WishlistItem, product=product, customer=request.user
    )

    wishlist_item.delete()

    return redirect(request.META.get("HTTP_REFERER", "/"))
