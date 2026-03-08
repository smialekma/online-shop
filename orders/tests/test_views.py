from django.test import TestCase, tag, override_settings
from django.urls import reverse

from carts.cart import Cart
from customers.factories import CustomerFactory
from orders.factories import ShippingMethodFactory
from orders.models import Order, OrderItem
from products.factories import ProductFactory, ProductImageFactory
import tempfile
import shutil

TEMP_MEDIA = tempfile.mkdtemp()


class CheckoutLoginViewTests(TestCase):

    def test_login_page_renders(self):
        response = self.client.get(reverse("checkout-login"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "orders/checkout_login.html")

    def test_redirect_authenticated_user(self):
        user = CustomerFactory()
        self.client.force_login(user)

        response = self.client.get(reverse("checkout-login"))

        self.assertRedirects(response, reverse("checkout-view"))


@tag("x")
@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class CheckoutViewTests(TestCase):

    def setUp(self):
        self.user = CustomerFactory()
        self.client.force_login(self.user)

        self.product = ProductFactory(price=10)
        ProductImageFactory(product=self.product, is_main_photo=True)

        self.shipping = ShippingMethodFactory(price=5)

        self.url = reverse("checkout-view")

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(TEMP_MEDIA)
        super().tearDownClass()

    def test_empty_cart_redirect(self):
        response = self.client.get(self.url)

        self.assertRedirects(response, reverse("home-view"))

    def add_product_to_cart(self):
        session = self.client.session
        cart = Cart(type("Request", (), {"session": session}))  # TODO
        cart.upsert(self.product, quantity=2)
        session.save()

    def test_checkout_creates_order(self):
        self.add_product_to_cart()

        data = {
            "email": "test@example.com",
            "shipping_method": self.shipping.id,
            "first_name": "John",
            "last_name": "Doe",
            "street": "Test Street",
            "city": "Warsaw",
            "postal_code": "00-001",
            "country": "PL",
        }

        self.client.post(self.url, data)

        order = Order.objects.first()

        self.assertIsNotNone(order)
        self.assertEqual(order.customer, self.user)

    def test_order_items_created_from_cart(self):
        self.add_product_to_cart()

        data = {
            "email": "test@example.com",
            "shipping_method": self.shipping.id,
            "first_name": "John",
            "last_name": "Doe",
            "street": "Test Street",
            "city": "Warsaw",
            "postal_code": "00-001",
            "country": "PL",
        }

        self.client.post(self.url, data)

        order = Order.objects.first()

        items = OrderItem.objects.filter(order=order)

        self.assertEqual(items.count(), 1)
        self.assertEqual(items.first().quantity, 2)

    def test_order_total_price(self):
        self.add_product_to_cart()

        data = {
            "email": "test@example.com",
            "shipping_method": self.shipping.id,
            "first_name": "John",
            "last_name": "Doe",
            "street": "Test Street",
            "city": "Warsaw",
            "postal_code": "00-001",
            "country": "PL",
        }

        self.client.post(self.url, data)

        order = Order.objects.first()

        # 2 * 10 + 5 shipping
        self.assertEqual(order.total_amount, 25)

    def test_cart_is_cleared_after_checkout(self):
        self.add_product_to_cart()

        data = {
            "email": "test@example.com",
            "shipping_method": self.shipping.id,
            "first_name": "John",
            "last_name": "Doe",
            "street": "Test Street",
            "city": "Warsaw",
            "postal_code": "00-001",
            "country": "PL",
        }

        self.client.post(self.url, data)

        session = self.client.session
        cart = Cart(type("Request", (), {"session": session}))

        self.assertEqual(len(cart), 0)

    def test_redirect_to_payment(self):
        self.add_product_to_cart()

        data = {
            "email": "test@example.com",
            "shipping_method": self.shipping.id,
            "first_name": "John",
            "last_name": "Doe",
            "street": "Test Street",
            "city": "Warsaw",
            "postal_code": "00-001",
            "country": "PL",
        }

        response = self.client.post(self.url, data)

        order = Order.objects.first()

        self.assertRedirects(response, reverse("stripe-view", args=[order.id]))
