from django import forms

from newsletter.models import Subscriber


class SubscriberUpdateForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = "__all__"
        widgets = {
            "date_subscribed": forms.DateInput(attrs={"type": "datetime-local"}),
        }
