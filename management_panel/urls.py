from django.urls import path

from management_panel.views.list_views import (
    OrderManagementListView,
    BrandManagementListView,
    CategoryManagementListView,
    ReviewManagementListView,
    PaymentManagementListView,
    ProductManagementListView,
    ShippingMethodManagementListView,
    UserManagementListView,
)
from management_panel.views.panel_view import ManagementPanelView
from management_panel.views.update_views import (
    OrderUpdateView,
    BrandUpdateView,
    ReviewUpdateView,
    CategoryUpdateView,
    PaymentUpdateView,
    ProductUpdateView,
    ShippingMethodUpdateView,
    AddressUpdateView,
    UserUpdateView,
)

urlpatterns = [
    path("", ManagementPanelView.as_view(), name="management-view"),
    path("orders/", OrderManagementListView.as_view(), name="management-orders"),
    path("orders/<int:pk>", OrderUpdateView.as_view(), name="management-orders-update"),
    path("brands/", BrandManagementListView.as_view(), name="management-brands"),
    path("brands/<int:pk>", BrandUpdateView.as_view(), name="management-brands-update"),
    path(
        "categories/",
        CategoryManagementListView.as_view(),
        name="management-categories",
    ),
    path(
        "categories/<int:pk>",
        CategoryUpdateView.as_view(),
        name="management-categories-update",
    ),
    path("reviews/", ReviewManagementListView.as_view(), name="management-reviews"),
    path(
        "reviews/<int:pk>", ReviewUpdateView.as_view(), name="management-reviews-update"
    ),
    path("payments/", PaymentManagementListView.as_view(), name="management-payments"),
    path(
        "payments/<int:pk>",
        PaymentUpdateView.as_view(),
        name="management-payments-update",
    ),
    path("products/", ProductManagementListView.as_view(), name="management-products"),
    path(
        "products/<int:pk>",
        ProductUpdateView.as_view(),
        name="management-products-update",
    ),
    path(
        "shipping-methods/",
        ShippingMethodManagementListView.as_view(),
        name="management-shipping",
    ),
    path(
        "shipping-methods/<int:pk>",
        ShippingMethodUpdateView.as_view(),
        name="management-shipping-update",
    ),
    path(
        "addresses/<int:pk>",
        AddressUpdateView.as_view(),
        name="management-address-update",
    ),
    path("users/", UserManagementListView.as_view(), name="management-users"),
    path("users/<int:pk>", UserUpdateView.as_view(), name="management-users-update"),
]
