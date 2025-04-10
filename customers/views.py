from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages
from django.contrib.auth import views

from .forms import CustomerRegisterForm


class RegisterView(SuccessMessageMixin, CreateView):
    template_name = "customers/register.html"
    success_url = reverse_lazy("login-view")
    form_class = CustomerRegisterForm
    success_message = "You have been successfully registered."


class CustomLoginView(SuccessMessageMixin, views.LoginView):
    success_message = "You have been successfully login in."

    pass


class CustomLogoutView(views.LogoutView):
    success_message = "You have been successfully logged out."

    def post(self, request, *args, **kwargs):
        messages.success(request, self.success_message)

        return super().post(request, *args, **kwargs)
