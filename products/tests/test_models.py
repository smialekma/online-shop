import tempfile
from datetime import timedelta
from decimal import Decimal
from django.test import tag, override_settings
from PIL import Image
from django.test import TestCase
from django.utils import timezone

from orders.factories import OrderFactory, OrderItemFactory
from products.factories import ProductFactory
from products.models import ProductImage
import shutil
import tempfile
import os

TEMP_MEDIA = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class ProductModelTests(TestCase):
    @classmethod  # TODO change for if path.os.exists:
    def tearDownClass(cls) -> None:
        if os.path.exists:
            shutil.rmtree(TEMP_MEDIA)
        super().tearDownClass()

    def setUp(self):
        self.product = ProductFactory.create(
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


@tag("y")  # TODO tworzy plik w cateogry_pics
@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class ProductImageModelTests(TestCase):
    @classmethod  # TODO change for if path.os.exists:
    def tearDownClass(cls) -> None:
        shutil.rmtree(TEMP_MEDIA)
        super().tearDownClass()

    def setUp(self):
        self.product = ProductFactory.create()

    def test_image_save(self):
        img = Image.new("RGB", (800, 800))

        temp_path = os.path.join(TEMP_MEDIA, "test_image.jpg")

        img.save(temp_path)
        image = ProductImage.objects.create(
            product=self.product, photo="test_image.jpg", is_main_photo=True
        )

        self.assertIsNotNone(image.id)
