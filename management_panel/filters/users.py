import django_filters
from django.db.models import Q

from products.models import Product


class UserManagementFilter(django_filters.FilterSet):
    #  Search filter (by name or description)
    search = django_filters.CharFilter(method="filter_search", label="")

    is_active = django_filters.BooleanFilter(label="")
    is_manager = django_filters.BooleanFilter(label="")

    class Meta:
        model = Product
        fields = ["search", "is_active", "is_manager"]

    def filter_search(self, queryset, name, value):
        """Search by product name or description (case-insensitive)."""
        return queryset.filter(Q(username__icontains=value) | Q(email__icontains=value))
