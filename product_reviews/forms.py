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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields["rating"].empty_label = None
        # self.fields["rating"].initial = 5
        # self.fields["rating"].widget.attrs.update({"class": "input-rating"})
