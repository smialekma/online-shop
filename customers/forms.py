from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from customers.models import Customer


class CustomerRegisterForm(UserCreationForm):

    class Meta:
        model = Customer
        fields = ["email", "password1", "password2"]


class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False)
