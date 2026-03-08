from django.db.models import Count, Avg, F
from django.test import TestCase, tag, override_settings

from customers.factories import CustomerFactory
from orders.factories import OrderFactory, OrderItemFactory
from products.factories import ProductFactory
from products.models import Category, Product
from django.urls import reverse
import shutil
import tempfile

from ..management.commands.populate_db import Command
from ..views.dashboard_views import _get_random_products

TEMP_MEDIA = tempfile.mkdtemp()


@tag("x")
@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class RandomProductsTests(TestCase):

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(TEMP_MEDIA)
        super().tearDownClass()

    def test_returns_empty_queryset_when_no_products(self):
        products = _get_random_products(6)

        self.assertEqual(products.count(), 0)

    def test_returns_max_available_products(self):
        ProductFactory.create_batch(3)

        products = _get_random_products(6)

        self.assertEqual(products.count(), 3)

    def test_returns_exact_number_when_available(self):
        ProductFactory.create_batch(10)

        products = _get_random_products(6)

        self.assertEqual(products.count(), 6)


@tag("x")
@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class HomeViewTestCase(TestCase):
    def setUp(self) -> None:
        self.command = Command()
        self.brands = self.command.create_brands(5)
        self.categories = self.command.create_categories(5)
        self.command.create_products(
            5, brands=self.brands, categories=self.categories, is_sale=False
        )
        self.command.create_products(
            5, brands=self.brands, categories=self.categories, is_sale=True
        )
        # tworzysz usera
        # self.client.login(user)

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(TEMP_MEDIA)
        super().tearDownClass()

    def test_only_get_allowed(self) -> None:
        response = self.client.post(reverse("home-view"))
        self.assertEqual(response.status_code, 405)

        response = self.client.put(reverse("home-view"))
        self.assertEqual(response.status_code, 405)
        response = self.client.delete(reverse("home-view"))
        self.assertEqual(response.status_code, 405)
        response = self.client.patch(reverse("home-view"))
        self.assertEqual(response.status_code, 405)
        response = self.client.get(reverse("home-view"))
        self.assertEqual(response.status_code, 200)

    def test_home_view_category_display(self):
        categories = Category.objects.all().order_by("name")[:3]

        response = self.client.get(reverse("home-view"))

        for count, category in enumerate(response.context["category_display"]):
            self.assertEqual(category.pk, categories[count].pk)
            self.assertEqual(category.name, categories[count].name)

    def test_home_view_random_products(self):
        response = self.client.get(reverse("home-view"))

        self.assertEqual(response.context["random_products"].count(), 6)

    def test_home_view_discounted_products(self):
        response = self.client.get(reverse("home-view"))

        discounted_products = (
            Product.objects.all()
            .filter(is_sale=True)
            .select_related("category")
            .annotate(discount=F("old_price") - F("price"))
            .order_by("-discount")
        )[:6]

        tested_discounted_products = response.context["discounted_products"]

        self.assertEqual(tested_discounted_products.count(), 6)
        self.assertEqual(tested_discounted_products.first().is_sale, True)
        self.assertEqual(
            tested_discounted_products.first().discount,
            tested_discounted_products.first().old_price
            - tested_discounted_products.first().price,
        )
        self.assertEqual(
            tested_discounted_products.first().pk, discounted_products.first().pk
        )

    def test_home_view_top_rated_products(self):
        response = self.client.get(reverse("home-view"))

        products = (
            Product.objects.all()
            .select_related("category")
            .prefetch_related("reviews")
            .order_by("reviews__rating")[:6]
        )

        tested_products = response.context["top_rated_products"]

        self.assertEqual(tested_products.count(), 6)
        self.assertEqual(tested_products.first().pk, products.first().pk)

    def test_home_view_new_products(self):
        self.command.create_products(15, brands=self.brands, categories=self.categories)

        response = self.client.get(reverse("home-view"))

        new_products = response.context["new_products"]

        self.assertTrue(len(new_products) > 0)

        for category in self.categories:
            newest_product = (
                Product.objects.filter(category=category)
                .select_related("category")
                .order_by("-date_added")
                .first()
            )
            products_for_category = []
            is_newest_product = False
            for product in new_products:
                if product.category.pk == category.pk:
                    products_for_category.append(product)
                    if product.pk == newest_product.pk:
                        is_newest_product = True

            self.assertEqual(len(products_for_category), 5)
            self.assertEqual(is_newest_product, True)
            self.assertEqual(
                products_for_category[1].average_rating,
                Avg(products_for_category[1].reviews.rating),
            )

    def test_product_view_top_selling_products(self) -> None:
        self.command.create_products(15, brands=self.brands, categories=self.categories)

        response = self.client.get(reverse("home-view"))

        top_selling_products = response.context["top_selling_products"]

        for category in self.categories:
            top_selling_product = (
                Product.objects.filter(category=category.id)
                .select_related("category")
                .annotate(count=Count("order_items"))
                .order_by("-count")
                .first()
            )
            products_for_category = []
            is_top_selling = False
            for product in top_selling_products:
                if product.category.pk == category.pk:
                    products_for_category.append(product)
                    if product.pk == top_selling_product.pk:
                        is_top_selling = True

            self.assertEqual(len(products_for_category), 5)
            self.assertEqual(is_top_selling, True)
            self.assertEqual(
                products_for_category[1].average_rating,
                Avg(products_for_category[1].reviews.rating),
            )


class AccountViewTests(TestCase):

    def setUp(self):
        self.customer = CustomerFactory()
        self.url = reverse("account-view")

    def test_login_required(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login-view"))

    def test_account_statistics(self):
        self.client.force_login(self.customer)

        order = OrderFactory(customer=self.customer, total_amount=100)

        OrderItemFactory(order=order, quantity=2)
        OrderItemFactory(order=order, quantity=3)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total_orders"], 1)
        self.assertEqual(response.context["total_products"], 5)
        self.assertEqual(response.context["total_price"], 100)


class GlobalSearchViewTests(TestCase):

    def setUp(self):
        self.url = reverse("global-search")

        ProductFactory(name="Laptop Dell", description="Gaming laptop")
        ProductFactory(name="Phone", description="Smartphone device")

    def test_search_page_loads(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["products"], [])

    def test_search_returns_results(self):
        response = self.client.get(self.url, {"query": "Laptop"})

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.context["products"]), 0)

    def test_search_pagination(self):
        ProductFactory.create_batch(20, name="Keyboard")

        response = self.client.get(self.url, {"query": "Keyboard"})

        page_obj = response.context["page_obj"]

        self.assertTrue(page_obj.paginator.num_pages >= 2)
