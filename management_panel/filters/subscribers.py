import django_filters

from newsletter.models import Subscriber


class SubscriberManagementFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_search", label="")

    is_active = django_filters.BooleanFilter(label="")

    class Meta:
        model = Subscriber
        fields = ["search", "is_active"]

    def filter_search(self, queryset, name, value):
        return queryset.filter(email__icontains=value)
