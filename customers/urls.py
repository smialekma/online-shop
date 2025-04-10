from django.urls import path

from .views import RegisterView, CustomLoginView, CustomLogoutView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register-view"),
    path(
        "login/",
        CustomLoginView.as_view(template_name="customers/login.html"),
        name="login-view",
    ),
    path("logout/", CustomLogoutView.as_view(), name="logout-view"),
]
