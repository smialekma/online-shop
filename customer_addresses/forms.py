from typing import Any

from django import forms

from customer_addresses.models import CustomerAddress
from django.utils.safestring import mark_safe

from orders.models import ShippingMethod


class AddressForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomerAddress
        fields = [
            "email",
            "first_name",
            "last_name",
            "address_line",
            "telephone",
            "telephone",
            "postal_code",
            "city",
            "country",
        ]


class CheckoutForm(AddressForm):
    order_notes = forms.CharField(
        widget=forms.Textarea(attrs={"class": "input", "rows": 3}),
        required=False,
        max_length=300,
    )
    agree = forms.BooleanField(
        label=mark_safe(
            'I agree to the <a href="{% url "terms-view" %}" target="_blank">terms and conditions</a>'
        ),
        error_messages={"required": "You must accept the terms and conditions"},
        widget=forms.CheckboxInput(attrs={"class": "input-checkbox"}),
        required=True,
    )

    shipping_method = forms.ModelChoiceField(
        queryset=ShippingMethod.objects.all(),
        widget=forms.RadioSelect,
        required=True,
        label="Shipping method",
    )

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields["shipping_method"].label_from_instance = lambda obj: obj

    class Meta:
        model = CustomerAddress
        fields = [
            "email",
            "first_name",
            "last_name",
            "address_line",
            "telephone",
            "telephone",
            "postal_code",
            "city",
            "country",
            "order_notes",
            "agree",
            "shipping_method",
        ]

    def clean_agree(self) -> bool:
        agree: bool = self.cleaned_data.get("agree")

        if not agree:
            raise forms.ValidationError("You must accept the terms and conditions")

        return agree
