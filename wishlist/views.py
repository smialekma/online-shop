from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Avg
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, View

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


class AddToWishlistView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest) -> HttpResponseRedirect:
        product_id = request.POST.get("product_id")
        product = get_object_or_404(Product, id=product_id)

        _, created = WishlistItem.objects.get_or_create(
            product=product, customer=request.user
        )

        if created:
            messages.success(request, "Product was added to wishlist.")
        else:
            messages.error(request, "Product is already in your wishlist.")

        return self._redirect_back(request)

    def _redirect_back(self, request: HttpRequest) -> HttpResponseRedirect:
        return redirect(request.META.get("HTTP_REFERER", "/"))


class RemoveFromWishlistView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest) -> HttpResponseRedirect:
        product_id = request.POST.get("product_id")
        product = get_object_or_404(Product, id=product_id)

        item = WishlistItem.objects.filter(
            product=product, customer=request.user
        ).first()

        if item:
            item.delete()
            messages.success(request, "Product was removed from your wishlist.")
        else:
            messages.info(request, "This product is not in your wishlist.")

        return self._redirect_back(request)

    def _redirect_back(self, request: HttpRequest) -> HttpResponseRedirect:
        return redirect(request.META.get("HTTP_REFERER", "/"))
