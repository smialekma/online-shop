from unittest import TestCase

from product_reviews.factories import ReviewFactory
from product_reviews.models import Review


class TestReviewFactory(TestCase):
    def test_single_object_created(self) -> None:
        obj = ReviewFactory.create()

        review = Review.objects.get(pk=obj.pk)
        self.assertEqual(Review.objects.count(), 1)
        self.assertIsNotNone(review.name)

    def test_multiple_object_created(self) -> None:
        ReviewFactory.create(batch=5)
        self.assertEqual(Review.objects.count(), 5)
