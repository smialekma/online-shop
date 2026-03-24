from django.test import TestCase

from newsletter.factories import SubscriberFactory, NewsletterPostFactory
from newsletter.models import Subscriber, NewsletterPost


class TestSubscriberFactory(TestCase):
    def test_single_object_created(self) -> None:
        obj = SubscriberFactory.create()

        subscriber = Subscriber.objects.get(pk=obj.pk)
        self.assertEqual(Subscriber.objects.count(), 1)
        self.assertIsNotNone(subscriber.email)

    def test_multiple_object_created(self) -> None:
        SubscriberFactory.create_batch(5)
        self.assertEqual(Subscriber.objects.count(), 5)


class TestNewsletterPostFactory(TestCase):
    def test_single_object_created(self) -> None:
        obj = NewsletterPostFactory.create()

        post = NewsletterPost.objects.get(pk=obj.pk)
        self.assertEqual(NewsletterPost.objects.count(), 1)
        self.assertIsNotNone(post.title)

    def test_multiple_object_created(self) -> None:
        NewsletterPostFactory.create_batch(5)
        self.assertEqual(NewsletterPost.objects.count(), 5)
