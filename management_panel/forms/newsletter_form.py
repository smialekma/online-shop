from django import forms

from newsletter.models import NewsletterPost


class NewsletterUpdateForm(forms.ModelForm):
    class Meta:
        model = NewsletterPost
        fields = "__all__"
        widgets = {
            "created_at": forms.DateInput(attrs={"type": "datetime-local"}),
        }
