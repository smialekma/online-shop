from typing import Any

import django_filters
from django.db.models import Q, QuerySet

from products.models import Category, Brand, Product


class ProductManagementFilter(django_filters.FilterSet):
    #  Search filter (by name or description)
    search = django_filters.CharFilter(method="filter_search", label="")

    # 🏷 Brand & Category dropdowns (auto-generated choices)
    brand = django_filters.ModelChoiceFilter(
        field_name="brand", queryset=None, label=""
    )
    category = django_filters.ModelChoiceFilter(
        field_name="category", queryset=None, label=""
    )

    # Only products on sale
    is_sale = django_filters.BooleanFilter(label="")

    class Meta:
        model = Product
        fields = [
            "search",
            "brand",
            "category",
            "is_sale",
        ]

    def __init__(self, *args: tuple[Any], **kwargs: dict[str, Any]) -> None:
        super().__init__(*args, **kwargs)
        self.filters["brand"].queryset = Brand.objects.all().order_by("name")
        self.filters["category"].queryset = Category.objects.all().order_by("name")

    def filter_search(self, queryset: QuerySet, name: str, value: str) -> QuerySet:
        """Search by product name or description (case-insensitive)."""
        return queryset.filter(
            Q(name__icontains=value) | Q(description__icontains=value)
        )
