from datetime import timedelta

from django.test import TestCase, override_settings, tag
from django.urls import reverse
from django.utils import timezone

from customers.factories import CustomerFactory
from dashboard.management.commands.populate_db import Command
from orders.factories import ShippingMethodFactory, OrderFactory
from payments.factories import PaymentFactory
from product_reviews.factories import ReviewFactory
import tempfile
import shutil


TEMP_MEDIA = tempfile.mkdtemp()


@tag("x")
@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class ManagementPanelBaseTests(TestCase):

    def setUp(self):
        self.url = reverse("management-panel")
        self.manager = CustomerFactory(is_manager=True)

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(TEMP_MEDIA)
        super().tearDownClass()


class ManagementPanelAccessTests(ManagementPanelBaseTests):

    def test_login_required(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)

    def test_manager_can_access(self):
        self.client.force_login(self.manager)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_regular_user_cannot_access(self):
        user = CustomerFactory()

        self.client.force_login(user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 403)


class ManagementPanelContextTests(ManagementPanelBaseTests):

    def setUp(self):
        super().setUp()
        self.client.force_login(self.manager)

    def test_item_counts(self):
        command = Command()

        brands = command.create_brands(2)
        categories = command.create_categories(4)
        command.create_products(3, brands=brands, categories=categories)

        ShippingMethodFactory.create_batch(2)

        PaymentFactory(is_paid=False)
        PaymentFactory(is_paid=True)

        response = self.client.get(self.url)

        self.assertEqual(response.context["total_products"], 3)
        self.assertEqual(response.context["brands_count"], 2)
        self.assertEqual(response.context["categories_count"], 4)
        self.assertEqual(response.context["shipping_methods_count"], 2)
        self.assertEqual(response.context["pending_payments"], 1)

    def test_recent_items(self):
        ReviewFactory.create_batch(3)
        OrderFactory.create_batch(6)

        response = self.client.get(self.url)

        self.assertLessEqual(len(response.context["recent_reviews"]), 3)
        self.assertLessEqual(len(response.context["recent_orders"]), 6)

    def test_monthly_statistics(self):
        now = timezone.now()

        OrderFactory(created_at=now - timedelta(days=10))
        OrderFactory(created_at=now - timedelta(days=40))

        PaymentFactory(
            is_paid=True,
            amount=100,
            created_at=now - timedelta(days=5),
        )

        PaymentFactory(
            is_paid=True,
            amount=50,
            created_at=now - timedelta(days=40),
        )

        response = self.client.get(self.url)

        self.assertEqual(response.context["orders_count_30d"], 1)
        self.assertEqual(response.context["revenue_30d"], 100)
