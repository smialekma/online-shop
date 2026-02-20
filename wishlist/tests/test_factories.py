from unittest import TestCase

from wishlist.factories import WishlistItemFactory
from wishlist.models import WishlistItem


class TestWishlistItemFactory(TestCase):
    def test_single_object_created(self) -> None:
        obj = WishlistItemFactory.create()

        item = WishlistItem.objects.get(pk=obj.pk)
        self.assertEqual(WishlistItem.objects.count(), 1)
        self.assertIsNotNone(item.name)

    def test_multiple_object_created(self) -> None:
        WishlistItemFactory.create(batch=5)
        self.assertEqual(WishlistItem.objects.count(), 5)
