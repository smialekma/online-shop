from django.test import RequestFactory, TestCase, tag, override_settings

from carts.cart import Cart
from core import settings
from products.factories import ProductImageFactory, ProductFactory
import tempfile
import shutil

TEMP_MEDIA = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class CartTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get("/")
        self.request.session = self.client.session

        self.product = ProductFactory(price=10, quantity=10)
        ProductImageFactory(product=self.product, is_main_photo=True)

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(TEMP_MEDIA)
        super().tearDownClass()

    def test_cart_initialization(self):
        cart = Cart(self.request)

        self.assertIn(settings.CART_SESSION_ID, self.request.session)
        self.assertEqual(len(cart.cart), 0)

    def test_upsert_new_product(self):
        cart = Cart(self.request)

        cart.upsert(self.product, quantity=2)

        item = cart.get_item(self.product.id)

        self.assertEqual(item["quantity"], 2)

    def test_upsert_increment_quantity(self):
        cart = Cart(self.request)

        cart.upsert(self.product, quantity=1)
        cart.upsert(self.product, quantity=2)

        item = cart.get_item(self.product.id)

        self.assertEqual(item["quantity"], 3)

    def test_upsert_override_quantity(self):
        cart = Cart(self.request)

        cart.upsert(self.product, quantity=5)
        cart.upsert(self.product, quantity=2, override_quantity=True)

        item = cart.get_item(self.product.id)

        self.assertEqual(item["quantity"], 2)

    def test_remove_product(self):
        cart = Cart(self.request)

        cart.upsert(self.product, quantity=2)
        cart.remove(self.product.id)

        self.assertIsNone(cart.get_item(self.product.id))

    def test_cart_len(self):
        cart = Cart(self.request)

        cart.upsert(self.product, quantity=3)

        self.assertEqual(len(cart), 3)

    def test_count_unique_items(self):
        cart = Cart(self.request)

        p2 = ProductFactory(price=5)

        cart.upsert(self.product)
        cart.upsert(p2)

        self.assertEqual(cart.count_unique_items(), 2)

    def test_cart_iteration(self):
        cart = Cart(self.request)

        cart.upsert(self.product, quantity=2)

        items = list(cart)

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["quantity"], 2)
        self.assertEqual(items[0]["product"]["id"], self.product.id)

    def test_get_sub_total_price(self):
        cart = Cart(self.request)

        cart.upsert(self.product, quantity=2)

        self.assertEqual(cart.get_sub_total_price(), 20)

    def test_get_total_price(self):
        cart = Cart(self.request)

        cart.upsert(self.product, quantity=3)

        self.assertEqual(cart.get_total_price(), 30)

    def test_clear_cart(self):
        cart = Cart(self.request)

        cart.upsert(self.product, quantity=2)

        cart.clear()

        self.assertEqual(len(cart), 0)
