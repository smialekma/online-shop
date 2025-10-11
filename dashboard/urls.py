from django.urls import path
from .views import HomeView, AccountView

urlpatterns = [
    path("", HomeView.as_view(), name="home-view"),
    path("account/", AccountView.as_view(), name="account-view"),
]
