from django.views.generic import TemplateView


class StaticPageView(TemplateView):
    template_name = "dashboard/terms.html"
    page_name = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = self.page_name
        return context


class TermsAndConditionsView(StaticPageView):
    page_name = "Terms & Conditions"


class AboutUsView(StaticPageView):
    page_name = "About Us"


class ContactUsView(StaticPageView):
    page_name = "Contact Us"


class PrivacyPolicyView(StaticPageView):
    page_name = "Privacy Policy"


class OrdersAndReturnsView(StaticPageView):
    page_name = "Orders & Returns"


class HelpView(StaticPageView):
    page_name = "Help"
