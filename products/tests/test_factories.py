from django.test import TestCase
from ..models import Brand, Category, Product, ProductImage
from ..factories import (
    BrandFactory,
    CategoryFactory,
    ProductFactory,
    ProductImageFactory,
)


class TestBrandFactory(TestCase):
    def test_single_object_created(self) -> None:
        obj = BrandFactory.create()

        brand = Brand.objects.get(pk=obj.pk)
        self.assertEqual(Brand.objects.count(), 1)
        self.assertIsNotNone(brand.name)

    def test_multiple_object_created(self) -> None:
        BrandFactory.create(batch=5)
        self.assertEqual(Brand.objects.count(), 5)


class TestCategoryFactory(TestCase):
    def test_single_object_created(self) -> None:
        obj = CategoryFactory.create()

        category = Category.objects.get(pk=obj.pk)
        self.assertEqual(Category.objects.count(), 1)
        self.assertIsNotNone(category.name)

    def test_multiple_object_created(self) -> None:
        CategoryFactory.create(batch=5)
        self.assertEqual(Category.objects.count(), 5)


class TestProductFactory(TestCase):
    def test_single_object_created(self) -> None:
        obj = ProductFactory.create()

        product = Product.objects.get(pk=obj.pk)
        self.assertEqual(Product.objects.count(), 1)
        self.assertIsNotNone(product.name)

    def test_multiple_object_created(self) -> None:
        ProductFactory.create(batch=5)
        self.assertEqual(Product.objects.count(), 5)


class TestProductImageFactory(TestCase):
    def test_single_object_created(self) -> None:
        obj = ProductImageFactory.create()

        img = ProductImage.objects.get(pk=obj.pk)
        self.assertEqual(ProductImage.objects.count(), 1)
        self.assertIsNotNone(img.name)

    def test_multiple_object_created(self) -> None:
        ProductImageFactory.create(batch=5)
        self.assertEqual(ProductImage.objects.count(), 5)
