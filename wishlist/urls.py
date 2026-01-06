from django.urls import path

from wishlist.views import WishlistView

urlpatterns = [
    path("wishlist/", WishlistView.as_view(), name="wishlist-view"),
]
