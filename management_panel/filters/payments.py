import django_filters
from django.db.models import Q
from django.forms import DateInput

from payments.models import Payment


class PaymentManagementFilter(django_filters.FilterSet):
    STATUS_CHOICES = (
        ("paid", "Paid"),
        ("unpaid", "Unpaid"),
    )

    search = django_filters.CharFilter(method="filter_search", label="")

    is_paid = django_filters.ChoiceFilter(
        method="filter_by_status", choices=STATUS_CHOICES, label=""
    )

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
        model = Payment
        fields = [
            "search",
            "is_paid",
            "date_from",
            "date_to",
        ]

    def filter_by_status(self, queryset, name, value):
        value = value.lower()
        if value == "paid":
            return queryset.filter(is_paid=True).distinct()
        elif value == "unpaid":
            return queryset.exclude(id__in=queryset.filter(is_paid=True)).distinct()
            # return queryset.exclude(payments__is_paid=True).distinct()
        return queryset

    def filter_search(self, queryset, name, value):
        """
        Search by Stripe checkout ID or related order number/ID.
        Adjust 'order__number' if your Order model uses that field.
        """
        return queryset.filter(
            Q(stripe_checkout_id__icontains=value) | Q(id__icontains=value)
        )
