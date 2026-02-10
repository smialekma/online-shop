from django.test import TestCase
from ..models import Brand


class TestBrandFactory(TestCase):
    def test_single_object_created(self):
        obj = Brand.objects.create()

        brand = Brand.objects.get(pk=obj.pk)
        self.assertEqual(Brand.objects.count(), 1)
        self.assertIsNotNone(brand.name)

    def test_multiple_object_created(self):
        Brand.objects.create(batch=5)
        self.assertEqual(Brand.objects.count(), 5)
