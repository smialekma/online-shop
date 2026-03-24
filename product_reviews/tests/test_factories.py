from dashboard.tests.test_dashboard_views import BaseTestClass
from product_reviews.factories import ReviewFactory
from product_reviews.models import Review


class TestReviewFactory(BaseTestClass):
    def test_single_object_created(self) -> None:
        obj = ReviewFactory.create()

        review = Review.objects.get(pk=obj.pk)
        self.assertEqual(Review.objects.count(), 1)
        self.assertIsNotNone(review.title)

    def test_multiple_object_created(self) -> None:
        ReviewFactory.create_batch(5)
        self.assertEqual(Review.objects.count(), 5)
