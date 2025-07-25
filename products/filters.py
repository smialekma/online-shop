import django_filters
from django import forms
from .models import Product, Category, Brand
from django.db.models import Count


class ProductFilter(django_filters.FilterSet):
    category = django_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.annotate(products_count=Count("products")),
        widget=forms.CheckboxSelectMultiple,
        label="Categories",
    )
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    brand = django_filters.ModelMultipleChoiceFilter(
        queryset=Brand.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Brands",
    )

    class Meta:
        model = Product
        fields = ["category", "brand"]
