from typing import Any

from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from customer_addresses.models import CustomerAddress
from customers.models import Customer
from management_panel.forms import (
    OrderUpdateForm,
    ReviewUpdateForm,
    PaymentUpdateForm,
    ProductUpdateForm,
    UserUpdateForm,
    SubscriberUpdateForm,
    NewsletterUpdateForm,
)
from management_panel.views.panel_view import ManagementBaseView
from newsletter.models import Subscriber, NewsletterPost
from orders.models import Order, OrderItem, ShippingMethod
from payments.models import Payment
from product_reviews.models import Review
from products.models import Brand, Product, Category


class OrderUpdateView(ManagementBaseView, UpdateView):
    model = Order
    template_name = "management_panel/update_order.html"
    form_class = OrderUpdateForm
    success_url = reverse_lazy("management-orders")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        order = self.get_object()
        context["items"] = OrderItem.objects.filter(order=order).select_related(
            "product"
        )
        return context

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()

        queryset = (
            queryset.select_related("address")
            .select_related("customer")
            .select_related("shipping_method")
        )

        return queryset


class AddressUpdateView(ManagementBaseView, UpdateView):
    model = CustomerAddress
    template_name = "management_panel/update_address.html"
    fields = "__all__"
    success_url = reverse_lazy("management-view")


class BrandUpdateView(ManagementBaseView, UpdateView):
    model = Brand
    template_name = "management_panel/update_brand.html"
    fields = "__all__"
    success_url = reverse_lazy("management-brands")


class ReviewUpdateView(ManagementBaseView, UpdateView):
    model = Review
    template_name = "management_panel/update_review.html"
    form_class = ReviewUpdateForm
    success_url = reverse_lazy("management-reviews")


class PaymentUpdateView(ManagementBaseView, UpdateView):
    model = Payment
    template_name = "management_panel/update_payment.html"
    form_class = PaymentUpdateForm
    success_url = reverse_lazy("management-payments")


class ProductUpdateView(ManagementBaseView, UpdateView):
    model = Product
    template_name = "management_panel/update_product.html"
    form_class = ProductUpdateForm
    success_url = reverse_lazy("management-products")


class ShippingMethodUpdateView(ManagementBaseView, UpdateView):
    model = ShippingMethod
    template_name = "management_panel/update_shipping.html"
    fields = "__all__"
    success_url = reverse_lazy("management-shipping")


class CategoryUpdateView(ManagementBaseView, UpdateView):
    model = Category
    template_name = "management_panel/update_category.html"
    fields = "__all__"
    success_url = reverse_lazy("management-categories")


class UserUpdateView(ManagementBaseView, UpdateView):
    model = Customer
    template_name = "management_panel/update_user.html"
    form_class = UserUpdateForm
    success_url = reverse_lazy("management-users")


class SubscriberUpdateView(ManagementBaseView, UpdateView):
    model = Subscriber
    template_name = "management_panel/update_subscriber.html"
    form_class = SubscriberUpdateForm
    success_url = reverse_lazy("management-subscribers")


class NewsletterUpdateView(ManagementBaseView, UpdateView):
    model = NewsletterPost
    template_name = "management_panel/update_newsletter.html"
    form_class = NewsletterUpdateForm
    success_url = reverse_lazy("management-newsletter")
