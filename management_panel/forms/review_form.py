from django import forms

from product_reviews.models import Review


class ReviewUpdateForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = "__all__"
        widgets = {
            "created_at": forms.DateInput(attrs={"type": "date"}),
        }
