from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages
from django.contrib.auth import views
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView

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


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = "customers/password_reset.html"
    email_template_name = "customers/password_reset_email.html"
    subject_template_name = "customers/password_reset_subject"
    success_message = (
        "We've emailed you instructions for setting your password, "
        "if an account exists with the email you entered, you should receive them shortly."
        " If you don't receive an email, "
        "please make sure you've entered the address you registered with, and check your spam folder."
    )
    success_url = reverse_lazy("home-view")


class CustomPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    success_url = reverse_lazy("home-view")
    success_message = "Your password has been set. You may now log in."
    template_name = "customers/password_reset_confirm.html"
