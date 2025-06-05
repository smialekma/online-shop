from django.urls import path
from .views import (
    RegisterView,
    CustomLoginView,
    CustomLogoutView,
    ResetPasswordView,
    CustomPasswordResetConfirmView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register-view"),
    path(
        "login/",
        CustomLoginView.as_view(template_name="customers/login.html"),
        name="login-view",
    ),
    path("logout/", CustomLogoutView.as_view(), name="logout-view"),
    path("password-reset/", ResetPasswordView.as_view(), name="password_reset"),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
]
