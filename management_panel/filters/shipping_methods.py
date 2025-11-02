import django_filters

from orders.models import ShippingMethod


class ShippingMethodManagementFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains", label="")

    class Meta:
        model = ShippingMethod
        fields = ["name"]
