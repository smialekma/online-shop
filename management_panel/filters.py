import django_filters
from django.db.models import Q
from django.forms import DateInput

from orders.models import Order, ShippingMethod
from payments.models import Payment
from product_reviews.models import Review
from products.models import Brand, Category, Product


class OrderManagementFilter(django_filters.FilterSet):
    STATUS_CHOICES = (
        ("paid", "Paid"),
        ("unpaid", "Unpaid"),
    )
    status = django_filters.ChoiceFilter(
        method="filter_by_status", choices=STATUS_CHOICES, label=""
    )

    search = django_filters.CharFilter(method="filter_search", label="")

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
        model = Order
        fields = ["created_at"]

    def filter_by_status(self, queryset, name, value):
        value = value.lower()
        if value == "paid":
            return queryset.filter(payments__is_paid=True).distinct()
        elif value == "unpaid":
            return queryset.exclude(
                id__in=queryset.filter(payments__is_paid=True)
            ).distinct()
            # return queryset.exclude(payments__is_paid=True).distinct()
        return queryset

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(id__icontains=value) | Q(customer__username__icontains=value)
        )


class BrandManagementFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains", label="")

    class Meta:
        model = Brand
        fields = ["name"]


class CategoryManagementFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains", label="")

    class Meta:
        model = Category
        fields = ["name"]


class ShippingMethodManagementFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains", label="")

    class Meta:
        model = ShippingMethod
        fields = ["name"]


class ProductManagementFilter(django_filters.FilterSet):
    #  Search filter (by name or description)
    search = django_filters.CharFilter(method="filter_search", label="")

    # 🏷 Brand & Category dropdowns (auto-generated choices)
    brand = django_filters.ModelChoiceFilter(
        field_name="brand", queryset=None, label=""
    )
    category = django_filters.ModelChoiceFilter(
        field_name="category", queryset=None, label=""
    )

    # 🛒 Only products on sale
    is_sale = django_filters.BooleanFilter(label="Tylko przecenione")

    class Meta:
        model = Product
        fields = [
            "search",
            "brand",
            "category",
            "is_sale",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters["brand"].queryset = Brand.objects.all().order_by("name")
        self.filters["category"].queryset = Category.objects.all().order_by("name")

    def filter_search(self, queryset, name, value):
        """Search by product name or description (case-insensitive)."""
        return queryset.filter(
            Q(name__icontains=value) | Q(description__icontains=value)
        )


class PaymentManagementFilter(django_filters.FilterSet):
    # Search filter — looks through Stripe ID or order ID
    search = django_filters.CharFilter(method="filter_search", label="")

    # Paid / not paid
    is_paid = django_filters.BooleanFilter(label="")

    # 🕒 Date range
    date_from = django_filters.DateFilter(
        field_name="created_at", lookup_expr="gte", label="Data od"
    )
    date_to = django_filters.DateFilter(
        field_name="created_at", lookup_expr="lte", label="Data do"
    )

    class Meta:
        model = Payment
        fields = [
            "search",
            "is_paid",
            "date_from",
            "date_to",
        ]

    def filter_search(self, queryset, name, value):
        """
        Search by Stripe checkout ID or related order number/ID.
        Adjust 'order__number' if your Order model uses that field.
        """
        return queryset.filter(
            Q(stripe_checkout_id__icontains=value) | Q(id__icontains=value)
        )


class ReviewManagementFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_search", label="")

    # Rating filter (exact match or minimum rating)
    rating = django_filters.ChoiceFilter(choices=Review.RATING_CHOICES, label="")

    date_from = django_filters.DateFilter(
        field_name="created_at", lookup_expr="gte", label="Data od"
    )
    date_to = django_filters.DateFilter(
        field_name="created_at", lookup_expr="lte", label="Data do"
    )

    class Meta:
        model = Review
        fields = [
            "search",
            "rating",
            "date_from",
            "date_to",
        ]

    def filter_search(self, queryset, name, value):
        """Search in username."""
        return queryset.filter(author__username__icontains=value)
