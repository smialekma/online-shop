from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from customer_addresses.forms import AddressForm
from customer_addresses.models import CustomerAddress


class AddressFormMixin:

    def save_address(self, form: AddressForm) -> CustomerAddress:
        new_address = form.save(commit=False)

        address_dct = {
            "first_name": new_address.first_name,
            "last_name": new_address.last_name,
            "address_line": new_address.address_line,
            "telephone": new_address.telephone,
            "postal_code": new_address.postal_code,
            "city": new_address.city,
            "country": new_address.country,
        }

        if self.request.user.is_authenticated:
            new_address = CustomerAddress.objects.update_or_create(
                defaults=address_dct, customer=self.request.user
            )[0]

        else:
            new_address = CustomerAddress.objects.create(**address_dct, customer=None)

        self.object = new_address

        return new_address

    def _get_address_or_none(self) -> CustomerAddress | None:
        try:
            address = (
                CustomerAddress.objects.filter(customer=self.request.user)
                .order_by("-id")
                .last()
            )
        except CustomerAddress.DoesNotExist:
            address = None

        return address

    def _populate_user_data(self, initial):
        initial["email"] = self.request.user.email

        address = self._get_address_or_none()

        if address:
            initial = self._populate_address_data(initial, address)

        return initial

    def _populate_address_data(self, initial, address):
        address_fields = [
            "first_name",
            "last_name",
            "address_line",
            "telephone",
            "postal_code",
            "city",
            "country",
        ]

        for field in address_fields:
            if hasattr(address, field):
                initial[field] = getattr(address, field)

        return initial


class EditAddressView(
    AddressFormMixin, SuccessMessageMixin, LoginRequiredMixin, CreateView
):
    model = CustomerAddress
    template_name = "customer_addresses/edit_address.html"
    form_class = AddressForm
    success_message = "The address has been successfully saved."
    success_url = reverse_lazy("account-view")

    def form_valid(self, form: AddressForm) -> HttpResponseRedirect:
        self.save_address(form)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        url = reverse_lazy("account-view")
        return HttpResponseRedirect(url)

    def get_initial(self, *args, **kwargs):
        initial = super().get_initial()

        initial = self._populate_user_data(initial)

        return initial
