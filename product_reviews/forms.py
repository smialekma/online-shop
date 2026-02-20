from django import forms
from product_reviews.models import Review


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=Review.RATING_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "rating-radio"}),
    )

    class Meta:
        model = Review
        fields = ["title", "body", "rating"]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "input",
                    "placeholder": "Review title",
                }
            ),
            "body": forms.Textarea(
                attrs={
                    "class": "input",
                    "placeholder": "Write your review here...",
                    "rows": 3,
                }
            ),
        }
