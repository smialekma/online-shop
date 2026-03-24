from django.db.models import QuerySet, Count, Avg
from django.test import TestCase, tag, override_settings, RequestFactory

from carts.cart import Cart
from customers.factories import CustomerFactory
from product_reviews.factories import ReviewFactory
from product_reviews.models import Review
from ..factories import (
    ProductFactory,
    BrandFactory,
    CategoryFactory,
    ProductImageFactory,


)
from product_reviews.factories import ReviewFactory
from django.urls import reverse
import shutil
import tempfile
import os
from ..views import _get_available_amount_of_product

TEMP_MEDIA = tempfile.mkdtemp()


@tag("x")
@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class ProductViewTestCase(TestCase):
    def setUp(self) -> None:
        self.products = sorted(ProductFactory.create_batch(30), key=lambda p: p.date_added, reverse=True)
        # tworzysz usera
        # self.client.login(user)

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(TEMP_MEDIA)
        super().tearDownClass()

    def test_only_get_allowed(self) -> None:
        response = self.client.post(reverse("product-view"))
        self.assertEqual(response.status_code, 405)

        response = self.client.put(reverse("product-view"))
        self.assertEqual(response.status_code, 405)
        response = self.client.delete(reverse("product-view"))
        self.assertEqual(response.status_code, 405)
        response = self.client.patch(reverse("product-view"))
        self.assertEqual(response.status_code, 405)
        response = self.client.get(reverse("product-view"))
        self.assertEqual(response.status_code, 200)

    def test_product_view_return_products_without_filters(self) -> None:
        response = self.client.get(reverse("product-view"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/products.html")
        self.assertIn("products", response.context)
        self.assertIn("filter", response.context)
        self.assertEqual(len(response.context["products"]), 12)

    def test_product_view_pagination_first_page(self) -> None:
        response = self.client.get(reverse("product-view"))

        self.assertEqual(len(response.context["products"]), 12)

    def test_product_view_pagination_second_page(self) -> None:
        response = self.client.get(reverse("product-view") + "?page=2")

        self.assertEqual(len(response.context["products"]), 12)

    def test_product_view_pagination_last_page(self) -> None:
        response = self.client.get(reverse("product-view") + "?page=3")

        self.assertEqual(len(response.context["products"]), 6)

    def test_product_view_ordering_by_date_added(self) -> None:
        response = self.client.get(reverse("product-view"))
        products = response.context["products"]

        self.assertGreater(products[0].date_added, products[1].date_added)
        self.assertGreater(products[7].date_added, products[10].date_added)

    # def test_product_view_top_selling_products(self) -> None:
    #     response = self.client.get(reverse("product-view"))
    #     top_selling_products = response.context["top_selling_products"]
    #     all_products: QuerySet = response.context["products"]
    #
    #     self.assertEqual(len(top_selling_products), 3)
    #
    #     expected_pks = all_products.object_list.annotate(count=Count("order_items")).order_by("-count").values_list("pk", flat=True)[:3]
    #
    #
    #     self.assertQuerySetEqual(
    #         top_selling_products.values_list("pk", flat=True), expected_pks
    #     )

    def test_product_view_with_filter_parameters(self) -> None:
        brand = BrandFactory.create(name="test_brand", pk=31)
        category = CategoryFactory.create(name="test_category", pk=31)
        ProductFactory.create(category=category, brand=brand, price=3959.79, pk=31)

        response = self.client.get(
            reverse("product-view")
            + "?category=31&min_price=3000.01&max_price=3999.98&brand=31"
        )
        products = response.context["products"]

        self.assertTrue(len(products) == 1)
        self.assertEqual(products[0].category.pk, 31)
        self.assertEqual(products[0].brand.pk, 31)
        self.assertTrue(products[0].price >= 3000.01)
        self.assertTrue(products[0].price <= 3999.98)

    def test_product_view_products_have_avarage_rating_annotation(self) -> None:
        product = self.products[0]
        print(product.pk)
        ReviewFactory.create(product=product)
        product.refresh_from_db()

        response = self.client.get(reverse("product-view"))
        products: QuerySet = response.context["products"]
        product_from_view = products[0]

        ratings = [review.rating for review in product.reviews.all()]
        expected_avg = sum(ratings) / len(ratings)

        self.assertEqual(product_from_view.average_rating, expected_avg)

    def test_product_view_invalid_page_numer(self) -> None:
        pass

        # def setUp(self):

    #     self.factory = RequestFactory()
    #     self.view = ProductView()
    #
    # def test_model_is_product(self):
    #     self.assertEqual(ProductView.model, Product)
    #
    # def test_template_name(self):
    #     self.assertEqual(ProductView.template_name, 'products/products.html')

    # @patch('products.views.ProductFilter')
    # @patch('products.views.Product.objects.all')
    # def test_get_context_data_filter_creation(self, mock_product_all, mock_filter_class):
    #     # Arrange
    #     request = self.factory.get('/products/', {'category': '1'})
    #     self.view.request = request
    #     self.view.object_list = Mock()
    #
    #     mock_queryset = Mock()
    #     mock_product_all.return_value.prefetch_related.return.return_value.annotate.return_value = mock_queryset
    #     mock_filter_instance = Mock()
    #     mock_filter_instance.qs = Mock()
    #
    #     mock_filter_class.return_value = mock_filter_instance
    #
    #     # Act
    #     context = self.view.get_context_data()
    #
    #     # Assert
    #     mock_filter_class.assert_called_once()


@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class ProductDetailViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.product = ProductFactory.create(quantity=10)
        ProductImageFactory(product=cls.product, is_main_photo=True)
        customers = CustomerFactory.create_batch(25)
        cls.reviews = [ReviewFactory(product=cls.product, author=customers[i])
                       for i in range(25)]
        cls.url = reverse("detail-view", args=[cls.product.id])

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(TEMP_MEDIA)
        super().tearDownClass()

    def test_product_detail_renders(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/product_details.html")

    def test_reviews_in_context(self):
        response = self.client.get(self.url)

        self.assertIn("reviews", response.context)
        self.assertEqual(len(response.context["reviews"]), 10)

    def test_review_creation(self):
        user = CustomerFactory()
        self.client.force_login(user)

        response = self.client.post(
            self.url, {"rating": 5, "body": "Great product", "title": "Great"}
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.url)

    def test_reviews_ordered_by_date_created(self):
        response = self.client.get(self.url)
        latest_review = (
            Review.objects.filter(product_id=self.product.id)
            .order_by("-created_at")
            .first()
        )

        tested_reviews = response.context["reviews"]
        self.assertEqual(tested_reviews[0].pk, latest_review.pk)

    def test_pagination_first_page(self) -> None:
        response = self.client.get(self.url)

        self.assertEqual(len(response.context["reviews"]), 10)

    def test_pagination_second_page(self) -> None:
        response = self.client.get(self.url + "?page=2")

        self.assertEqual(len(response.context["reviews"]), 10)

    def test_pagination_last_page(self) -> None:
        response = self.client.get(self.url + "?page=3")

        self.assertEqual(len(response.context["reviews"]), 5)

    def test_review_aggregations(self):
        review_aggregations = (
            Review.objects.filter(product=self.product)
            .order_by("-created_at")
            .aggregate(average_rating=Avg("rating"), review_count=Count("id"))
        )

        print(review_aggregations)

        response = self.client.get(self.url)
        tested_aggregations = response.context["review_aggregations"]

        self.assertEqual(tested_aggregations["average_rating"], review_aggregations["average_rating"])
        self.assertEqual(tested_aggregations["review_count"], review_aggregations["review_count"])

    def test_related_products(self):
        pass

@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class AddToCartTests(TestCase):

    def setUp(self):
        self.product = ProductFactory.create(quantity=10, price=10)
        self.url = reverse("product-add")

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(TEMP_MEDIA)
        super().tearDownClass()

    def test_add_product_to_cart(self):
        response = self.client.post(self.url, {"product_id": self.product.id})

        self.assertEqual(response.status_code, 200)

        session = self.client.session
        cart = Cart(type("Request", (), {"session": session}))

        self.assertEqual(len(cart), 1)

    def test_add_to_cart_out_of_stock(self):
        product = ProductFactory(quantity=0)

        response = self.client.post(self.url, {"product_id": product.id})

        self.assertTrue(response.json()["limited"])

@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class AddToCartWithQtyTests(TestCase):

    def setUp(self):
        self.product = ProductFactory.create(quantity=5)
        self.url = reverse("detail-add", args=[self.product.id])

    @classmethod
    def tearDownClass(cls) -> None:
        if os.path.exists(TEMP_MEDIA):
            shutil.rmtree(TEMP_MEDIA)
        super().tearDownClass()

    def test_add_quantity(self):
        self.client.post(self.url, {"quantity": 2}, HTTP_REFERER="/")

        session = self.client.session
        cart = Cart(type("Request", (), {"session": session}))

        self.assertEqual(len(cart), 2)

    def test_add_more_than_stock(self):
        self.client.post(self.url, {"quantity": 10}, HTTP_REFERER="/")

        session = self.client.session
        cart = Cart(type("Request", (), {"session": session}))

        self.assertEqual(len(cart), 5)


@tag("x")
@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class RemoveFromCartTests(TestCase):

    def setUp(self):
        self.product = ProductFactory(quantity=10)
        self.url = reverse("product-remove")

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(TEMP_MEDIA)
        super().tearDownClass()

    def test_remove_product(self):
        session = self.client.session
        cart = Cart(type("Request", (), {"session": session}))
        cart.upsert(self.product, 3)
        session.save()

        self.client.post(self.url, {"product_id": self.product.id})

        session = self.client.session
        cart = Cart(type("Request", (), {"session": session}))

        self.assertEqual(len(cart), 0)


@tag("x")
@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class ProductStockLogicTests(TestCase):

    def setUp(self):
        self.product = ProductFactory(quantity=5)
        self.request = RequestFactory().get("/")
        self.request.session = self.client.session

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(TEMP_MEDIA)
        super().tearDownClass()

    def test_available_quantity(self):
        cart = Cart(self.request)

        result = _get_available_amount_of_product(cart, self.product, 2)

        self.assertEqual(result, 2)

    def test_quantity_limited_by_stock(self):
        cart = Cart(self.request)

        result = _get_available_amount_of_product(cart, self.product, 10)

        self.assertEqual(result, 5)
