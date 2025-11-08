from django import forms

from customers.models import Customer


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
        widgets = {
            "date_joined": forms.DateInput(attrs={"type": "datetime-local"}),
            "last_login": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
