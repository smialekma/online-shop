from typing import Any

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView
from django.contrib import messages
from django.contrib.auth import views
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView

from .forms import CustomerRegisterForm
from .models import Customer
from .tokens import account_activation_token


class RegisterView(SuccessMessageMixin, CreateView):
    template_name = "customers/register.html"
    success_url = reverse_lazy("home-view")
    form_class = CustomerRegisterForm
    success_message = (
        "You have been successfully registered. "
        "We've emailed you instructions for activating your account. "
        "If an account exists with the email you entered, you should receive them shortly. "
        "If you don't receive an email, "
        "please make sure you've entered the correct email address, and check your spam folder."
    )

    def form_valid(self, form: CustomerRegisterForm) -> Any:
        customer = form.save(commit=False)
        customer.save()

        current_site = get_current_site(self.request)
        mail_subject = "Online Shop - activate your account"
        message = render_to_string(
            "customers/register_activation_email.html",
            {
                "customer": customer,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(customer.pk)),
                "token": account_activation_token.make_token(customer),
            },
        )
        to_email = form.cleaned_data.get("email")
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()

        return super().form_valid(form)


class CustomLoginView(SuccessMessageMixin, views.LoginView):
    success_message = "You have been successfully logged in."


class CustomLogoutView(views.LogoutView):
    success_message = "You have been successfully logged out."

    def post(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponseRedirect | TemplateResponse:
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


def activate(request: HttpRequest, uidb64: str, token: str) -> HttpResponseRedirect:
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = Customer.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Customer.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save(updated_fields=["is_active"])
        messages.success(
            request, "Your account has been activated. You may now log in."
        )
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect("login-view")
