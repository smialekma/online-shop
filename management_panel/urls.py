from django.urls import path

from management_panel.views import (
    ManagementPanelView,
    OrderManagementListView,
    BrandManagementListView,
    CategoryManagementListView,
    ReviewManagementListView,
    PaymentManagementListView,
    ProductManagementListView,
    ShippingMethodManagementListView,
)

urlpatterns = [
    path("", ManagementPanelView.as_view(), name="management-view"),
    path("orders/", OrderManagementListView.as_view(), name="management-orders"),
    path("brands/", BrandManagementListView.as_view(), name="management-brands"),
    path(
        "categories/",
        CategoryManagementListView.as_view(),
        name="management-categories",
    ),
    path("reviews/", ReviewManagementListView.as_view(), name="management-reviews"),
    path("payments/", PaymentManagementListView.as_view(), name="management-payments"),
    path("products/", ProductManagementListView.as_view(), name="management-products"),
    path(
        "shipping-methods/",
        ShippingMethodManagementListView.as_view(),
        name="management-shipping",
    ),
]
