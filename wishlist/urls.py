from django.urls import path

from wishlist.views import WishlistView, AddToWishlistView, RemoveFromWishlistView

urlpatterns = [
    path("wishlist/", WishlistView.as_view(), name="wishlist-view"),
    path("wishlist/add", AddToWishlistView.as_view(), name="wishlist-add"),
    path("wishlist/remove", RemoveFromWishlistView.as_view(), name="wishlist-remove"),
]
