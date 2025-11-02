import django_filters

from products.models import Category


class CategoryManagementFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains", label="")

    class Meta:
        model = Category
        fields = ["name"]
