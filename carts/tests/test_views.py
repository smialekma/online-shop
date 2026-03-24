import json

from django.contrib.messages import get_messages
from django.urls import reverse
from django.test import TestCase, tag, override_settings

from carts.cart import Cart
from products.factories import ProductFactory, ProductImageFactory
import tempfile
import shutil
from unittest.mock import Mock

TEMP_MEDIA = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class CartViewTests(TestCase):

    def setUp(self):
        self.product = ProductFactory(price=10, quantity=10)
        ProductImageFactory(product=self.product, is_main_photo=True)

        self.url = reverse("cart-view")

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(TEMP_MEDIA)
        super().tearDownClass()

    def test_cart_view_renders(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "carts/cart.html")

    def test_cart_products_in_context(self):
        request = Mock()
        request.session = self.client.session

        cart = Cart(request)
        cart.upsert(self.product, quantity=2)
        request.session.save()

        response = self.client.get(self.url)

        self.assertEqual(len(response.context["products"]), 1)


@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class CartUpdateTests(TestCase):

    def setUp(self):
        self.product = ProductFactory(price=10, quantity=10)
        ProductImageFactory(product=self.product, is_main_photo=True)

        self.url = reverse("cart-update")

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(TEMP_MEDIA)
        super().tearDownClass()

    @tag("fail")
    def test_update_cart_quantity(self):
        request = Mock()
        request.session = self.client.session

        cart = Cart(request)
        cart.upsert(self.product, quantity=1)
        request.session.save()

        response = self.client.post(
            self.url,
            data=json.dumps({"product_id": self.product.id, "quantity": 3}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context["cart"]), 3)

    def test_update_limited_by_stock(self):
        product = ProductFactory(price=10, quantity=2)

        request = Mock()
        request.session = self.client.session

        cart = Cart(request)
        cart.upsert(product, quantity=1)
        request.session.save()

        response = self.client.post(
            self.url,
            data=json.dumps({"product_id": product.id, "quantity": 10}),
            content_type="application/json",
        )

        self.assertTrue(response.json()["limited"])

    def test_product_not_found(self):
        response = self.client.post(
            self.url,
            data=json.dumps({"product_id": 9999, "quantity": 2}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 404)


@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class RemoveFromCartViewTests(TestCase):

    def setUp(self):
        self.product = ProductFactory(price=10, quantity=10)

        self.url = reverse("cart-remove")

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(TEMP_MEDIA)
        super().tearDownClass()

    def test_remove_product_from_cart(self):
        session = self.client.session
        cart = Cart(type("Request", (), {"session": session}))
        cart.upsert(self.product, quantity=1)
        session.save()

        self.client.post(
            self.url,
            {"product_id": self.product.id},
            HTTP_REFERER="/",
        )

        session = self.client.session
        cart = Cart(type("Request", (), {"session": session}))

        self.assertEqual(len(cart), 0)

    def test_success_message(self):
        session = self.client.session
        cart = Cart(type("Request", (), {"session": session}))
        cart.upsert(self.product, quantity=1)
        session.save()

        response = self.client.post(
            self.url, {"product_id": self.product.id}, HTTP_REFERER="/", follow=True
        )

        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(any("removed from your cart" in str(m) for m in messages))
