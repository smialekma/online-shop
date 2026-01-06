from django import forms

from newsletter.models import Subscriber


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ["email"]
