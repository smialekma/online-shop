from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from wishlist.models import WishlistItem


class WishlistView(LoginRequiredMixin, ListView):
    template_name = "wishlist/wishlist.html"
    model = WishlistItem
    context_object_name = "items"
    ordering = "-date_added"
    paginate_by = 5

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context_data = super().get_context_data(**kwargs)
        context_data["rating_options"] = (1, 2, 3, 4, 5)

        return context_data

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.is_authenticated:
            return queryset.select_related("product").filter(customer=self.request.user)
        else:
            return []
