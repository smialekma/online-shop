from django.urls import path

from wishlist.views import WishlistView, add_to_wishlist, remove_from_wishlist

urlpatterns = [
    path("wishlist/", WishlistView.as_view(), name="wishlist-view"),
    path("wishlist/add", add_to_wishlist, name="wishlist-add"),
    path("wishlist/remove", remove_from_wishlist, name="wishlist-remove"),
]
