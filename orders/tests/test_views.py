from unittest.mock import Mock

from django.test import TestCase, tag, override_settings
from django.urls import reverse

from carts.cart import Cart
from customer_addresses.forms import CheckoutForm
from customers.factories import CustomerFactory
from dashboard.tests.test_dashboard_views import BaseTestClass
from orders.factories import ShippingMethodFactory, OrderFactory
from orders.models import Order, OrderItem
from products.factories import ProductFactory, ProductImageFactory
import tempfile
import shutil

TEMP_MEDIA = tempfile.mkdtemp()


class CheckoutLoginViewTests(BaseTestClass):

    def _add_product_to_cart(self):
        request = Mock()
        request.session = self.client.session
        product = ProductFactory()

        cart = Cart(request)
        cart.upsert(product, quantity=2)
        request.session.save()

    def test_login_page_renders(self):
        response = self.client.get(reverse("checkout-login"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "orders/checkout_login.html")

    def test_redirect_authenticated_user(self):
        user = CustomerFactory()
        self.client.force_login(user)

        self._add_product_to_cart()

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
        self.order = OrderFactory.build(
            customer=self.user, shipping_method=self.shipping
        )
        self.valid_data = dict(
            email=self.order.email,
            first_name=self.order.address.first_name,
            last_name=self.order.address.last_name,
            address_line=self.order.address.address_line,
            telephone=self.order.address.telephone,
            postal_code=self.order.address.postal_code,
            city=self.order.address.city,
            country=self.order.address.country,
            order_notes=self.order.order_notes,
            agree=True,
            shipping_method=self.order.shipping_method.id,
        )

        self.url = reverse("checkout-view")

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(TEMP_MEDIA)
        super().tearDownClass()

    def test_empty_cart_redirect(self):
        response = self.client.get(self.url)

        self.assertRedirects(response, reverse("home-view"))

    def add_product_to_cart(self):
        request = Mock()
        request.session = self.client.session

        cart = Cart(request)  # TODO
        cart.upsert(self.product, quantity=2)
        request.session.save()

    def test_checkout_creates_order(self):
        self.add_product_to_cart()

        self.client.post(self.url, self.valid_data)

        order = Order.objects.first()

        self.assertIsNotNone(order)
        self.assertEqual(order.customer, self.user)

    def test_order_items_created_from_cart(self):
        self.add_product_to_cart()

        self.client.post(self.url, self.valid_data)

        CheckoutForm(data=self.valid_data)

        order = Order.objects.prefetch_related("order_items").first()

        items = OrderItem.objects.filter(order=order)

        self.assertEqual(items.count(), 1)
        self.assertEqual(items.first().quantity, 2)

    def test_cart_is_cleared_after_checkout(self):
        self.add_product_to_cart()

        self.client.post(self.url, self.valid_data)
        request = Mock()
        request.session = self.client.session

        cart = Cart(request)

        self.assertEqual(len(cart), 0)

    def test_redirect_to_payment(self):
        self.add_product_to_cart()

        response = self.client.post(self.url, self.valid_data)

        self.assertEqual(response.status_code, 302)
