from django.http import HttpRequest

from .models import WishlistItem


def wishlist_items(request: HttpRequest) -> dict[str, list[int | None]]:
    if request.user.is_authenticated:
        items = (
            WishlistItem.objects.filter(customer=request.user)
            .select_related("product")
            .order_by("-date_added")
        )
        product_ids = [item.product.id for item in items]

        return {"wishlist_items": product_ids}
    return {"wishlist_items": []}
