import django_filters
from django.db.models import QuerySet

from .models import Order


class OrderFilter(django_filters.FilterSet):
    STATUS_CHOICES = (
        ("paid", "Paid"),
        ("unpaid", "Unpaid"),
    )
    status = django_filters.ChoiceFilter(
        method="filter_by_status", choices=STATUS_CHOICES, label=""
    )

    search = django_filters.CharFilter(method="filter_search", label="")

    order_by = django_filters.OrderingFilter(
        label="",
        fields=[
            ("date_ordered", "date_ordered"),
            ("total_amount", "total_amount"),
        ],
        field_labels={
            "date_ordered": "Date",
            "total_amount": "Total amount",
        },
    )

    class Meta:
        model = Order

    def filter_by_status(self, queryset: QuerySet, name: str, value: str) -> QuerySet:
        value = value.lower()
        if value == "paid":
            return queryset.filter(payments__is_paid=True).distinct()
        elif value == "unpaid":
            return queryset.exclude(
                id__in=queryset.filter(payments__is_paid=True)
            ).distinct()
            # return queryset.exclude(payments__is_paid=True).distinct()
        return queryset

    def filter_search(self, queryset: QuerySet, name: str, value: str) -> QuerySet:
        return queryset.filter(order_items__product__name__icontains=value)
