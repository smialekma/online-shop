from django.urls import path
from .views import HomeView, AccountView, GlobalSearchView

urlpatterns = [
    path("", HomeView.as_view(), name="home-view"),
    path("account/", AccountView.as_view(), name="account-view"),
    path("search/", GlobalSearchView.as_view(), name="global-search"),
]
