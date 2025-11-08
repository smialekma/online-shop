from django import forms

from payments.models import Payment


class PaymentUpdateForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = "__all__"
        widgets = {
            "created_at": forms.DateInput(attrs={"type": "date"}),
        }
