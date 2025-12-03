import django_filters
from django.forms import DateInput

from newsletter.models import NewsletterPost


class NewsletterManagementFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_search", label="")

    is_published = django_filters.BooleanFilter(label="")
    to_publish = django_filters.BooleanFilter(label="")

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
        model = NewsletterPost
        fields = [
            "search",
            "is_published",
            "to_publish",
            "date_from",
            "date_to",
        ]

    def filter_search(self, queryset, name, value):
        return queryset.filter(title__icontains=value)
