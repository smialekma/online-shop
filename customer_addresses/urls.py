from django.urls import path

from customer_addresses.views import EditAddressView

urlpatterns = [
    path("address/", EditAddressView.as_view(), name="edit-address-view"),
]
