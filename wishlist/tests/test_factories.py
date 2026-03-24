from django.test import TestCase

from dashboard.tests.test_dashboard_views import BaseTestClass
from wishlist.factories import WishlistItemFactory
from wishlist.models import WishlistItem


class TestWishlistItemFactory(BaseTestClass):
    def test_single_object_created(self) -> None:
        obj = WishlistItemFactory.create()

        item = WishlistItem.objects.get(pk=obj.pk)
        self.assertEqual(WishlistItem.objects.count(), 1)
        self.assertIsNotNone(item.product.name)

    def test_multiple_object_created(self) -> None:
        WishlistItemFactory.create_batch(5)
        self.assertEqual(WishlistItem.objects.count(), 5)
