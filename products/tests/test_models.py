import tempfile
from datetime import timedelta
from decimal import Decimal

from PIL import Image
from django.test import TestCase
from django.utils import timezone

from orders.factories import OrderFactory, OrderItemFactory
from products.factories import ProductFactory
from products.models import ProductImage


class ProductModelTests(TestCase):

    def setUp(self):
        self.product = ProductFactory(
            name="Laptop", price=Decimal("100"), old_price=Decimal("200")
        )

    def test_str_returns_name(self):
        self.assertEqual(str(self.product), "Laptop")

    def test_product_is_new(self):
        self.product.date_added = timezone.now() - timedelta(days=5)

        self.assertTrue(self.product.is_new())

    def test_product_is_not_new(self):
        self.product.date_added = timezone.now() - timedelta(days=15)

        self.assertFalse(self.product.is_new())

    def test_sale_percentage(self):
        percent = self.product.sale_percentage()

        self.assertEqual(percent, 50)

    def test_get_related_products(self):
        product2 = ProductFactory()
        product3 = ProductFactory()

        order = OrderFactory()

        OrderItemFactory(order=order, product=self.product)
        OrderItemFactory(order=order, product=product2)
        OrderItemFactory(order=order, product=product3)

        related = self.product.get_related_products(limit=2)

        self.assertTrue(len(related) <= 2)

        product_ids = [item["product"].id for item in related]

        self.assertIn(product2.id, product_ids)


class ProductImageModelTests(TestCase):

    def setUp(self):
        self.product = ProductFactory()

    def test_image_save(self):
        img = Image.new("RGB", (800, 800))

        temp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
        img.save(temp_file.name)

        image = ProductImage.objects.create(
            product=self.product, photo=temp_file.name, is_main_photo=True
        )

        self.assertIsNotNone(image.id)
