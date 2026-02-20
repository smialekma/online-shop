from django.db import models

from customers.models import Customer


class CustomerAddress(models.Model):
    customer: models.ForeignKey = models.ForeignKey(
        Customer,
        related_name="addresses",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    first_name: str | models.CharField = models.CharField(max_length=100)
    last_name: str | models.CharField = models.CharField(max_length=100)
    address_line: str | models.CharField = models.CharField(max_length=100)
    telephone: str | models.CharField = models.CharField(max_length=100)
    postal_code: str | models.CharField = models.CharField(max_length=20)
    city: str | models.CharField = models.CharField(max_length=100)
    country: str | models.CharField = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.address_line}"

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
