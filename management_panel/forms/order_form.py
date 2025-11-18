from django import forms

from orders.models import Order


class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"
        widgets = {
            "date_ordered": forms.DateInput(attrs={"type": "date"}),
            "date_fulfilled": forms.DateInput(attrs={"type": "date"}),
            "created_at": forms.DateInput(attrs={"type": "date"}),
            "updated_at": forms.DateInput(attrs={"type": "date"}),
        }
