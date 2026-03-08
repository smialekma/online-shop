from django.contrib.messages import get_messages
from django.test import TestCase, override_settings, tag
from django.urls import reverse

from customers.factories import CustomerFactory
from products.factories import ProductFactory
from wishlist.factories import WishlistItemFactory
import tempfile
import shutil

from wishlist.models import WishlistItem

TEMP_MEDIA = tempfile.mkdtemp()


@tag("x")
@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class WishlistViewTests(TestCase):

    def setUp(self):
        self.user = CustomerFactory()
        self.other_user = CustomerFactory()

        self.product = ProductFactory()

        WishlistItemFactory(customer=self.user, product=self.product)
        WishlistItemFactory(customer=self.other_user, product=self.product)

        self.url = reverse("wishlist-view")

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(TEMP_MEDIA)
        super().tearDownClass()

    def test_login_required(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)

    def test_only_user_items_displayed(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        items = response.context["items"]

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].customer, self.user)


@tag("x")
@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class AddToWishlistTests(TestCase):

    def setUp(self):
        self.user = CustomerFactory()
        self.product = ProductFactory()

        self.url = reverse("wishlist-add")

        self.client.force_login(self.user)

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(TEMP_MEDIA)
        super().tearDownClass()

    def test_add_product_to_wishlist(self):
        self.client.post(self.url, {"product_id": self.product.id}, HTTP_REFERER="/")

        self.assertTrue(
            WishlistItem.objects.filter(
                product=self.product, customer=self.user
            ).exists()
        )

    def test_add_duplicate_product(self):
        WishlistItemFactory(customer=self.user, product=self.product)

        self.client.post(self.url, {"product_id": self.product.id}, HTTP_REFERER="/")

        items = WishlistItem.objects.filter(product=self.product, customer=self.user)

        self.assertEqual(items.count(), 1)

    def test_success_message(self):
        response = self.client.post(
            self.url, {"product_id": self.product.id}, HTTP_REFERER="/", follow=True
        )

        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(any("added to wishlist" in str(m) for m in messages))


@tag("x")
@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class RemoveFromWishlistTests(TestCase):

    def setUp(self):
        self.user = CustomerFactory()
        self.product = ProductFactory()

        self.item = WishlistItemFactory(customer=self.user, product=self.product)

        self.url = reverse("wishlist-remove")

        self.client.force_login(self.user)

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(TEMP_MEDIA)
        super().tearDownClass()

    def test_remove_product(self):
        self.client.post(self.url, {"product_id": self.product.id}, HTTP_REFERER="/")

        self.assertFalse(
            WishlistItem.objects.filter(
                product=self.product, customer=self.user
            ).exists()
        )

    def test_remove_non_existing_item(self):
        WishlistItem.objects.all().delete()

        response = self.client.post(
            self.url, {"product_id": self.product.id}, HTTP_REFERER="/", follow=True
        )

        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(any("not in your wishlist" in str(m) for m in messages))
