import shutil

from django.test import TestCase, tag, override_settings
from django.urls import reverse

from customers.factories import CustomerFactory
from management_panel.tests.test_panel_view import ManagementPanelAccessTests

# TODO

from newsletter.factories import SubscriberFactory, NewsletterPostFactory
from orders.factories import OrderFactory, ShippingMethodFactory
from payments.factories import PaymentFactory
from product_reviews.factories import ReviewFactory
from products.factories import BrandFactory, CategoryFactory, ProductFactory
import tempfile

TEMP_MEDIA = tempfile.mkdtemp()


@tag("x")
@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class ManagementViewsBaseTest(TestCase, ManagementPanelAccessTests):

    def setUp(self):
        self.admin = CustomerFactory(is_manager=True)
        self.client.force_login(self.admin)

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(TEMP_MEDIA)
        super().tearDownClass()


class OrderManagementListViewTests(ManagementViewsBaseTest):

    def setUp(self):
        super().setUp()
        self.url = reverse("management-orders")

    def test_orders_list_view(self):
        OrderFactory.create_batch(5)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "management_panel/management_orders.html")
        self.assertIn("orders", response.context)

    def test_pagination(self):
        OrderFactory.create_batch(30)

        response = self.client.get(self.url)

        self.assertEqual(len(response.context["products"]), 20)


class BrandManagementListViewTests(ManagementViewsBaseTest):

    def setUp(self):
        super().setUp()
        self.url = reverse("management-brands")

    def test_brands_list(self):
        BrandFactory.create_batch(3)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("brands", response.context)

    def test_pagination(self):
        BrandFactory.create_batch(30)

        response = self.client.get(self.url)

        self.assertEqual(len(response.context["products"]), 20)


class CategoryManagementListViewTests(ManagementViewsBaseTest):

    def setUp(self):
        super().setUp()
        self.url = reverse("management-categories")

    def test_categories_list(self):
        CategoryFactory.create_batch(3)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("categories", response.context)

    def test_pagination(self):
        CategoryFactory.create_batch(30)

        response = self.client.get(self.url)

        self.assertEqual(len(response.context["products"]), 20)


class ReviewManagementListViewTests(ManagementViewsBaseTest):

    def setUp(self):
        super().setUp()
        self.url = reverse("management-reviews")

    def test_reviews_list(self):
        ReviewFactory.create_batch(3)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("reviews", response.context)

    def test_pagination(self):
        ReviewFactory.create_batch(30)

        response = self.client.get(self.url)

        self.assertEqual(len(response.context["products"]), 20)


class PaymentManagementListViewTests(ManagementViewsBaseTest):

    def setUp(self):
        super().setUp()
        self.url = reverse("management-payments")

    def test_payments_list(self):
        PaymentFactory.create_batch(3)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("payments", response.context)

    def test_pagination(self):
        PaymentFactory.create_batch(30)

        response = self.client.get(self.url)

        self.assertEqual(len(response.context["products"]), 20)


class ProductManagementListViewTests(ManagementViewsBaseTest):

    def setUp(self):
        super().setUp()
        self.url = reverse("management-products")

    def test_products_list(self):
        ProductFactory.create_batch(3)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("products", response.context)

    def test_pagination(self):
        ProductFactory.create_batch(30)

        response = self.client.get(self.url)

        self.assertEqual(len(response.context["products"]), 20)


class ShippingMethodManagementListViewTests(ManagementViewsBaseTest):

    def setUp(self):
        super().setUp()
        self.url = reverse("management-shipping")

    def test_shipping_methods(self):
        ShippingMethodFactory.create_batch(3)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("methods", response.context)

    def test_pagination(self):
        ShippingMethodFactory.create_batch(30)

        response = self.client.get(self.url)

        self.assertEqual(len(response.context["products"]), 20)


class UserManagementListViewTests(ManagementViewsBaseTest):

    def setUp(self):
        super().setUp()
        self.url = reverse("management-users")

    def test_users_list(self):
        CustomerFactory.create_batch(3)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("users", response.context)

    def test_pagination(self):
        CustomerFactory.create_batch(30)

        response = self.client.get(self.url)

        self.assertEqual(len(response.context["products"]), 20)


class SubscriberManagementListViewTests(ManagementViewsBaseTest):

    def setUp(self):
        super().setUp()
        self.url = reverse("management-subscribers")

    def test_subscribers_list(self):
        SubscriberFactory.create_batch(3)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("subscribers", response.context)

    def test_pagination(self):
        SubscriberFactory.create_batch(30)

        response = self.client.get(self.url)

        self.assertEqual(len(response.context["products"]), 20)


class NewsletterManagementListViewTests(ManagementViewsBaseTest):

    def setUp(self):
        super().setUp()
        self.url = reverse("management-newsletter")

    def test_newsletter_posts(self):
        NewsletterPostFactory.create_batch(3)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("posts", response.context)

    def test_pagination(self):
        NewsletterPostFactory.create_batch(30)

        response = self.client.get(self.url)

        self.assertEqual(len(response.context["products"]), 20)
