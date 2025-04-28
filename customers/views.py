from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages
from django.contrib.auth import views

from .forms import CustomerRegisterForm, LoginForm


class RegisterView(SuccessMessageMixin, CreateView):
    template_name = "customers/register.html"
    success_url = reverse_lazy("login-view")
    form_class = CustomerRegisterForm
    success_message = "You have been successfully registered."


class CustomLoginView(SuccessMessageMixin, views.LoginView):
    success_message = "You have been successfully logged in."
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data["remember_me"]
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super(CustomLoginView, self).form_valid(form)


class CustomLogoutView(views.LogoutView):
    success_message = "You have been successfully logged out."

    def post(self, request, *args, **kwargs):
        messages.success(request, self.success_message)

        return super().post(request, *args, **kwargs)
