from django.test import TestCase
from ..factories import ProductFactory
from django.urls import reverse


class ProductViewTestCase(TestCase):
    def setUp(self):
        ProductFactory.create_batch(10)
        # tworzysz usera
        # self.client.login(user)

    def test_only_get_allowed(self):
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

    def test_product_view_return_products_without_filters(self):
        response = self.client.get(reverse("product-view"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/products.html")
        self.assertIn("products", response.context)
        self.assertIn("filter", response.context)
        self.assertEqual(len(response.context["products"]), 3)

    def test_product_view_pagination_first_page(self):
        pass

    def test_product_view_pagination_second_page(self):
        pass

    def test_product_view_pagination_last_page(self):
        pass

    def test_product_view_ordering_by_date_added(self):
        pass

    def test_product_view_top_selling_products(self):
        pass

    def test_product_view_with_filter_parameters(self):
        pass

    def test_product_view_products_have_avarage_rating_annotation(self):
        pass

    def test_product_view_invalid_page_numer(self):
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
