import django_filters
from django.db.models import Q
from django.forms import DateInput

from orders.models import Order


class OrderManagementFilter(django_filters.FilterSet):
    STATUS_CHOICES = (
        ("paid", "Paid"),
        ("unpaid", "Unpaid"),
    )
    status = django_filters.ChoiceFilter(
        method="filter_by_status", choices=STATUS_CHOICES, label=""
    )

    search = django_filters.CharFilter(method="filter_search", label="")

    date_from = django_filters.DateFilter(
        widget=DateInput(attrs={"type": "date"}),
        field_name="created_at",
        lookup_expr="gte",
        label="",
    )
    date_to = django_filters.DateFilter(
        widget=DateInput(attrs={"type": "date"}),
        field_name="created_at",
        lookup_expr="lte",
        label="",
    )

    class Meta:
        model = Order
        fields = ["created_at"]

    def filter_by_status(self, queryset, name, value):
        value = value.lower()
        if value == "paid":
            return queryset.filter(payments__is_paid=True).distinct()
        elif value == "unpaid":
            return queryset.exclude(
                id__in=queryset.filter(payments__is_paid=True)
            ).distinct()
            # return queryset.exclude(payments__is_paid=True).distinct()
        return queryset

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(id__icontains=value) | Q(customer__username__icontains=value)
        )
