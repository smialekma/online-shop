from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum
from django.views.generic import TemplateView
from django.utils import timezone

from orders.models import ShippingMethod, Order
from payments.models import Payment
from product_reviews.models import Review
from products.models import Product, Brand, Category


class ManagementPanelView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "management_panel/management_panel.html"

    def test_func(self):
        return self.request.user.is_manager or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context["total_products"] = Product.objects.count()
        context["brands_count"] = Brand.objects.count()
        context["categories_count"] = Category.objects.count()
        context["shipping_methods_count"] = ShippingMethod.objects.count()

        context["pending_payments"] = Payment.objects.filter(is_paid=False).count()

        today = timezone.now()
        today_minus_30d = today - timedelta(days=30)

        context["orders_count_30d"] = Order.objects.filter(
            created_at__gt=today_minus_30d
        ).count()
        context["revenue_30d"] = (
            Payment.objects.filter(
                is_paid=True, created_at__gt=today_minus_30d
            ).aggregate(Sum("amount"))["amount__sum"]
        ) or 0

        context["recent_orders"] = Order.objects.select_related("customer").order_by(
            "-created_at"
        )[:5]
        context["recent_reviews"] = Review.objects.select_related("author").order_by(
            "-created_at"
        )[:2]

        return context

    # def _get_recent_items(self):
    #     return {
    #         "recent_reviews": Review.objects.select_related("author").order_by("-created_at")[:2]
    #     }
