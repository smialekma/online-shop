import django_filters
from django.db.models import QuerySet
from django.forms import DateInput

from product_reviews.models import Review


class ReviewManagementFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_search", label="")

    # Rating filter (exact match or minimum rating)
    rating = django_filters.ChoiceFilter(
        choices=[(value, str(value)) for value, label in Review.RATING_CHOICES],
        label="",
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
        model = Review
        fields = [
            "search",
            "rating",
            "date_from",
            "date_to",
        ]

    def filter_search(self, queryset: QuerySet, name: str, value: str) -> QuerySet:
        """Search in username."""
        return queryset.filter(author__username__icontains=value)
