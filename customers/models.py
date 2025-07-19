from customer_addresses.models import CustomerAddress
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(UserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True")

        return super().create_superuser(username, email, password, **extra_fields)


class Customer(AbstractUser):  # AbstractBaseUser
    """User model."""

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(_("email address"), unique=True)
    address = models.ForeignKey(
        CustomerAddress,
        related_name="addresses",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()
