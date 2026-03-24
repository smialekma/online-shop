from django.test import TestCase, override_settings, tag
from django.urls import reverse

from customer_addresses.factories import CustomerAddressFactory
from customers.factories import CustomerFactory
from dashboard.tests.test_dashboard_views import BaseTestClass
from management_panel.tests.test_panel_view import ManagementPanelAccessTests
import tempfile
import shutil

from newsletter.factories import SubscriberFactory, NewsletterPostFactory
from orders.factories import OrderFactory, OrderItemFactory, ShippingMethodFactory
from payments.factories import PaymentFactory
from product_reviews.factories import ReviewFactory
from products.factories import ProductFactory, BrandFactory, CategoryFactory

TEMP_MEDIA = tempfile.mkdtemp()


class ManagementUpdateViewBase(ManagementPanelAccessTests):

    def setUp(self):
        self.manager = CustomerFactory(is_manager=True)
        self.client.force_login(self.manager)


class OrderUpdateViewTests(ManagementUpdateViewBase):

    def setUp(self):
        super().setUp()
        self.order = OrderFactory()
        self.url = reverse("management-orders-update", args=[self.order.id])

    def test_order_update_view_loads(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "management_panel/update_order.html")

    def test_order_items_in_context(self):
        product = ProductFactory()
        OrderItemFactory(order=self.order, product=product)

        response = self.client.get(self.url)

        self.assertIn("items", response.context)
        self.assertEqual(len(response.context["items"]), 1)


class AddressUpdateViewTests(ManagementUpdateViewBase):

    def setUp(self):
        super().setUp()
        self.address = CustomerAddressFactory()
        self.url = reverse("management-address-update", args=[self.address.id])

    def test_address_update(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "management_panel/update_address.html")


class BrandUpdateViewTests(ManagementUpdateViewBase):

    def setUp(self):
        super().setUp()
        self.brand = BrandFactory()
        self.url = reverse("management-brands-update", args=[self.brand.id])

    def test_brand_update_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "management_panel/update_brand.html")


class ReviewUpdateViewTests(ManagementUpdateViewBase):

    def setUp(self):
        super().setUp()
        self.review = ReviewFactory()
        self.url = reverse("management-reviews-update", args=[self.review.id])

    def test_review_update_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "management_panel/update_review.html")


class PaymentUpdateViewTests(ManagementUpdateViewBase):

    def setUp(self):
        super().setUp()
        self.payment = PaymentFactory()
        self.url = reverse("management-payments-update", args=[self.payment.id])

    def test_payment_update_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "management_panel/update_payment.html")


class ProductUpdateViewTests(ManagementUpdateViewBase):

    def setUp(self):
        super().setUp()
        self.product = ProductFactory()
        self.url = reverse("management-products-update", args=[self.product.id])

    def test_product_update_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "management_panel/update_product.html")


class ShippingMethodUpdateViewTests(ManagementUpdateViewBase):

    def setUp(self):
        super().setUp()
        self.method = ShippingMethodFactory()
        self.url = reverse("management-shipping-update", args=[self.method.id])

    def test_shipping_method_update_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "management_panel/update_shipping.html")


class CategoryUpdateViewTests(ManagementUpdateViewBase):

    def setUp(self):
        super().setUp()
        self.category = CategoryFactory()
        self.url = reverse("management-categories-update", args=[self.category.id])

    def test_category_update_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "management_panel/update_category.html")


class UserUpdateViewTests(ManagementUpdateViewBase):

    def setUp(self):
        super().setUp()
        self.user = CustomerFactory()
        self.url = reverse("management-users-update", args=[self.user.id])

    def test_user_update_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "management_panel/update_user.html")


class SubscriberUpdateViewTests(ManagementUpdateViewBase):

    def setUp(self):
        super().setUp()
        self.subscriber = SubscriberFactory()
        self.url = reverse("management-subscribers-update", args=[self.subscriber.id])

    def test_subscriber_update_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "management_panel/update_subscriber.html")


class NewsletterUpdateViewTests(ManagementUpdateViewBase):

    def setUp(self):
        super().setUp()
        self.post = NewsletterPostFactory()
        self.url = reverse("management-newsletter-update", args=[self.post.id])

    def test_newsletter_update_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "management_panel/update_newsletter.html")
