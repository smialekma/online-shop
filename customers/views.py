from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView

from .forms import UserRegisterForm


class RegisterView(SuccessMessageMixin, CreateView):
    template_name = "customers/register.html"
    form_class = UserRegisterForm
    success_url = ""
    success_message = "You have been successfully registered."
