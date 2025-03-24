import django_filters
from django import forms
from .models import Product, Category


class ProductFilter(django_filters.FilterSet):
    category = django_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Categories",
    )
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    brand = django_filters.AllValuesMultipleFilter(
        field_name="brand", widget=forms.CheckboxSelectMultiple
    )
    # ModelMultipleChoiceFilter(
    #    queryset=Product.objects.all().only('brand').distinct().order_by("brand"),
    #    widget=forms.CheckboxSelectMultiple,
    #    label='Brands'))

    class Meta:
        model = Product
        fields = ["category", "brand"]
