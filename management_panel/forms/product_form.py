from django import forms

from products.models import Product


class ProductUpdateForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            "date_added": forms.DateInput(attrs={"type": "date"}),
        }
