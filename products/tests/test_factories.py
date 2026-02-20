from django.test import TestCase
from ..models import Brand
from ..factories import BrandFactory


class TestBrandFactory(TestCase):
    def test_single_object_created(self) -> None:
        obj = BrandFactory.create()

        brand = Brand.objects.get(pk=obj.pk)
        self.assertEqual(Brand.objects.count(), 1)
        self.assertIsNotNone(brand.name)

    def test_multiple_object_created(self) -> None:
        BrandFactory.create(batch=5)
        self.assertEqual(Brand.objects.count(), 5)
