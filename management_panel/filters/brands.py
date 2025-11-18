import django_filters

from products.models import Brand


class BrandManagementFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains", label="")

    class Meta:
        model = Brand
        fields = ["name"]
