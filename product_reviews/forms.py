from django import forms
from product_reviews.models import Review

RATING_CHOICES = (
    (5, "star5"),
    (4, "star4"),
    (3, "star3"),
    (2, "star2"),
    (1, "star1"),
)


class ReviewForm(forms.ModelForm):

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
            "rating": forms.RadioSelect(
                choices=RATING_CHOICES, attrs={"class": "rating-radio"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["rating"].widget.attrs.update({"class": "input-rating"})
