from typing import Any

from django.views.generic import TemplateView


class TermsAndConditionsView(TemplateView):
    template_name = "dashboard/terms.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["name"] = "Terms & Conditions"

        return context


class AboutUsView(TemplateView):
    template_name = "dashboard/terms.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["name"] = "About Us"

        return context


class ContactUsView(TemplateView):
    template_name = "dashboard/terms.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["name"] = "Contact Us"

        return context


class PrivacyPolicyView(TemplateView):
    template_name = "dashboard/terms.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["name"] = "Privacy Policy"

        return context


class OrdersAndReturnsView(TemplateView):
    template_name = "dashboard/terms.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["name"] = "Orders & Returns"

        return context


class HelpView(TemplateView):
    template_name = "dashboard/terms.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["name"] = "Help"

        return context
