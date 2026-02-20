from django.db.models import QuerySet
from django.http import HttpRequest

from .models import Category


def categories(request: HttpRequest) -> dict[str, QuerySet]:
    return {
        "categories": Category.objects.all()
        .prefetch_related("products")
        .order_by("name")
    }
