from django.contrib.auth.forms import UserCreationForm

from customers.models import Customer


class CustomerRegisterForm(UserCreationForm):

    class Meta:
        model = Customer
        fields = ["email", "password1", "password2"]
