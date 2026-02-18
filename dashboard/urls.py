from django.urls import path
from dashboard.views.dashboard_views import HomeView, AccountView, GlobalSearchView
from dashboard.views.doc_views import (
    TermsAndConditionsView,
    AboutUsView,
    HelpView,
    ContactUsView,
    OrdersAndReturnsView,
    PrivacyPolicyView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home-view"),
    path("account/", AccountView.as_view(), name="account-view"),
    path("search/", GlobalSearchView.as_view(), name="global-search"),
    path("terms/", TermsAndConditionsView.as_view(), name="terms-view"),
    path("about/", AboutUsView.as_view(), name="about-view"),
    path("help/", HelpView.as_view(), name="help-view"),
    path("contact/", ContactUsView.as_view(), name="contact-view"),
    path("orders/", OrdersAndReturnsView.as_view(), name="returns-view"),
    path("policy/", PrivacyPolicyView.as_view(), name="policy-view"),
]
