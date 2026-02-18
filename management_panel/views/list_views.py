from django.db.models import QuerySet
from django.views.generic import ListView
from django_filters.views import FilterView


from customers.models import Customer
from management_panel.filters import (
    ShippingMethodManagementFilter,
    UserManagementFilter,
    ProductManagementFilter,
    PaymentManagementFilter,
    ReviewManagementFilter,
    CategoryManagementFilter,
    BrandManagementFilter,
    OrderManagementFilter,
    NewsletterManagementFilter,
)
from management_panel.filters.subscribers import SubscriberManagementFilter
from management_panel.views.panel_view import ManagementBaseView
from newsletter.models import Subscriber, NewsletterPost
from orders.models import ShippingMethod, Order
from payments.models import Payment
from product_reviews.models import Review
from products.models import Product, Category, Brand


class OrderManagementListView(ManagementBaseView, FilterView, ListView):
    template_name = "management_panel/management_orders.html"
    model = Order
    filterset_class = OrderManagementFilter
    context_object_name = "orders"
    ordering = "-created_at"
    paginate_by = 20

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()

        queryset = queryset.select_related("customer")

        return queryset


class BrandManagementListView(ManagementBaseView, FilterView, ListView):
    template_name = "management_panel/management_brands.html"
    model = Brand
    filterset_class = BrandManagementFilter
    context_object_name = "brands"
    ordering = "name"
    paginate_by = 20


class CategoryManagementListView(ManagementBaseView, FilterView, ListView):
    template_name = "management_panel/management_categories.html"
    model = Category
    filterset_class = CategoryManagementFilter
    context_object_name = "categories"
    ordering = "-name"
    paginate_by = 20


class ReviewManagementListView(ManagementBaseView, FilterView, ListView):
    template_name = "management_panel/management_reviews.html"
    model = Review
    filterset_class = ReviewManagementFilter
    context_object_name = "reviews"
    ordering = "-created_at"
    paginate_by = 20

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()

        queryset = queryset.select_related("author").select_related("product")

        return queryset


class PaymentManagementListView(ManagementBaseView, FilterView, ListView):
    template_name = "management_panel/management_payments.html"
    model = Payment
    filterset_class = PaymentManagementFilter
    context_object_name = "payments"
    ordering = "-created_at"
    paginate_by = 20

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()

        queryset = queryset.select_related("order")

        return queryset


class ProductManagementListView(ManagementBaseView, FilterView, ListView):
    template_name = "management_panel/management_products.html"
    model = Product
    filterset_class = ProductManagementFilter
    context_object_name = "products"
    ordering = "-date_added"
    paginate_by = 20

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()

        queryset = queryset.select_related("brand").select_related("category")

        return queryset


class ShippingMethodManagementListView(ManagementBaseView, FilterView, ListView):
    template_name = "management_panel/management_shipping.html"
    model = ShippingMethod
    filterset_class = ShippingMethodManagementFilter
    context_object_name = "methods"
    ordering = "-name"
    paginate_by = 20


class UserManagementListView(ManagementBaseView, FilterView, ListView):
    template_name = "management_panel/management_users.html"
    model = Customer
    filterset_class = UserManagementFilter
    context_object_name = "users"
    ordering = "username"
    paginate_by = 20


class SubscriberManagementListView(ManagementBaseView, FilterView, ListView):
    template_name = "management_panel/management_subscribers.html"
    model = Subscriber
    filterset_class = SubscriberManagementFilter
    context_object_name = "subscribers"
    ordering = "-date_subscribed"
    paginate_by = 20


class NewsletterManagementListView(ManagementBaseView, FilterView, ListView):
    template_name = "management_panel/management_newsletter.html"
    model = NewsletterPost
    filterset_class = NewsletterManagementFilter
    context_object_name = "posts"
    ordering = "-created_at"
    paginate_by = 20
