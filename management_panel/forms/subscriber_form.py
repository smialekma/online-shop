from django import forms

from newsletter.models import Subscriber


class SubscriberUpdateForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ["email", "is_active", "date_subscribed"]
        widgets = {
            "date_subscribed": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
