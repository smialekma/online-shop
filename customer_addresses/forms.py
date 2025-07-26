from django import forms

from customer_addresses.models import CustomerAddress


class AddressForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    order_notes = forms.CharField(
        widget=forms.Textarea(attrs={"class": "input", "rows": 3}),
        required=False,
        max_length=300,
    )
    agree = forms.BooleanField(
        label='I agree to the <a href="/terms/" target="_blank">terms and conditions</a>',
        error_messages={"required": "You must accept the terms and conditions"},
        widget=forms.CheckboxInput(attrs={"class": "input-checkbox"}),
        required=True,
    )

    class Meta:
        model = CustomerAddress
        fields = "__all__"

    def clean_agree(self):
        agree = self.cleaned_data.get("agree")

        if not agree:
            raise forms.ValidationError("You must accept the terms and conditions")

        return agree
