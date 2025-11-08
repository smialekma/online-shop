from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum
from django.utils import timezone
from django.views.generic import TemplateView

from orders.models import Order, ShippingMethod
from payments.models import Payment
from product_reviews.models import Review
from products.models import Product, Brand, Category


class ManagementBaseView(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_manager or self.request.user.is_superuser


class ManagementPanelView(ManagementBaseView, TemplateView):
    template_name = "management_panel/management_panel.html"

    def test_func(self):
        return self.request.user.is_manager or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        recent_items = self._get_recent_items()
        monthly_statistics = self._get_item_monthly_statistics()
        item_counts = self._get_item_counts()

        context["total_products"] = item_counts["total_products"]
        context["brands_count"] = item_counts["brands_count"]
        context["categories_count"] = item_counts["categories_count"]
        context["shipping_methods_count"] = item_counts["shipping_methods_count"]

        context["pending_payments"] = item_counts["pending_payments"]

        context["orders_count_30d"] = monthly_statistics["orders_count_30d"]
        context["revenue_30d"] = monthly_statistics["revenue_30d"]

        context["recent_orders"] = recent_items["recent_orders"]
        context["recent_reviews"] = recent_items["recent_reviews"]

        return context

    def _get_recent_items(self):
        return {
            "recent_reviews": Review.objects.select_related("author").order_by(
                "-created_at"
            )[:2],
            "recent_orders": Order.objects.select_related("customer").order_by(
                "-created_at"
            )[:5],
        }

    def _get_item_counts(self):
        return {
            "total_products": Product.objects.count(),
            "brands_count": Brand.objects.count(),
            "categories_count": Category.objects.count(),
            "shipping_methods_count": ShippingMethod.objects.count(),
            "pending_payments": Payment.objects.filter(is_paid=False).count(),
        }

    def _get_item_monthly_statistics(self):
        today = timezone.now()
        today_minus_30d = today - timedelta(days=30)

        return {
            "orders_count_30d": Order.objects.filter(
                created_at__gt=today_minus_30d
            ).count(),
            "revenue_30d": (
                Payment.objects.filter(
                    is_paid=True, created_at__gt=today_minus_30d
                ).aggregate(Sum("amount"))["amount__sum"]
            )
            or 0,
        }
