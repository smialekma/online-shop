from django.test import TestCase
from ..models import Brand, Category, Product, ProductImage
from django.test import TestCase, tag, override_settings
from ..factories import (
    BrandFactory,
    CategoryFactory,
    ProductFactory,
    ProductImageFactory,
)
import shutil
import tempfile
import os

TEMP_MEDIA = tempfile.mkdtemp()


@tag('fast')
class TestBrandFactory(TestCase):
    def test_single_object_created(self) -> None:
        obj = BrandFactory.create()

        brand = Brand.objects.get(pk=obj.pk)
        self.assertEqual(Brand.objects.count(), 1)
        self.assertIsNotNone(brand.name)

    def test_multiple_object_created(self) -> None:
        BrandFactory.create_batch(5)
        self.assertEqual(Brand.objects.count(), 5)

@tag('fast')
@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class TestCategoryFactory(TestCase):
    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(TEMP_MEDIA)
        super().tearDownClass()
    def test_single_object_created(self) -> None:
        obj = CategoryFactory.create()

        category = Category.objects.get(pk=obj.pk)
        self.assertEqual(Category.objects.count(), 1)
        self.assertIsNotNone(category.name)

    def test_multiple_object_created(self) -> None:
        CategoryFactory.create_batch(5)
        self.assertEqual(Category.objects.count(), 5)
@tag('fast')
@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class TestProductFactory(TestCase):
    def test_single_object_created(self) -> None:
        obj = ProductFactory.create()

        product = Product.objects.get(pk=obj.pk)
        self.assertEqual(Product.objects.count(), 1)
        self.assertIsNotNone(product.name)

    def test_multiple_object_created(self) -> None:
        ProductFactory.create_batch(5)
        self.assertEqual(Product.objects.count(), 5)

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(TEMP_MEDIA)
        super().tearDownClass()
@tag('fast')
@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class TestProductImageFactory(TestCase):
    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(TEMP_MEDIA)
        super().tearDownClass()

    def test_single_object_created(self) -> None:
        obj = ProductImageFactory.create()

        img = ProductImage.objects.get(pk=obj.pk)
        self.assertEqual(ProductImage.objects.count(), 1)
        self.assertIsNotNone(img.product.name)

    def test_multiple_object_created(self) -> None:
        ProductImageFactory.create_batch(5)
        self.assertEqual(ProductImage.objects.count(), 5)
