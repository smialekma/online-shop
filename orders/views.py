from decimal import Decimal
from typing import Optional, Any, Coroutine

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import QuerySet
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from django_filters.views import FilterView

from carts.cart import Cart
from customer_addresses.forms import CheckoutForm
from customer_addresses.models import CustomerAddress
from customer_addresses.views import AddressFormMixin
from customers.views import CustomLoginView
from orders.filters import OrderFilter
from orders.models import Order, OrderItem, ShippingMethod
from django.http import HttpResponseRedirect, HttpResponseNotAllowed

from payments.models import Payment
from products.models import ProductImage


class CheckoutLoginView(CustomLoginView):
    template_name = "orders/checkout_login.html"
    next_page = reverse_lazy("checkout-view")
    redirect_authenticated_user = True


class CheckoutView(AddressFormMixin, CreateView):
    form_class = CheckoutForm
    template_name = "orders/checkout.html"
    success_url = reverse_lazy("stripe-view")

    def create_order(
        self,
        address: CustomerAddress,
        email: str,
        shipping_method: ShippingMethod,
        order_notes: Optional[str] = None,
    ) -> Order:
        cart = Cart(self.request)

        cart_total_price: Decimal = cart.get_total_price()
        order_total_price: Decimal = cart_total_price + Decimal(shipping_method.price)

        order: Order = Order.objects.create(
            address=address,
            total_amount=order_total_price,
            email=email,
            order_notes=order_notes,
            shipping_method=shipping_method,
        )

        if self.request.user.is_authenticated:
            order.customer = self.request.user

        order.save()
        return order

    def create_order_items_from_cart(self, order: Order) -> None:
        cart = Cart(self.request)
        for cart_item in cart:
            OrderItem.objects.create(
                order=order,
                product=cart_item["product"],  # __iter__
                quantity=cart_item["quantity"],
            )
        cart.clear()

    @transaction.atomic
    def form_valid(self, form: CheckoutForm) -> HttpResponseRedirect:
        new_address = self.save_address(form)

        shipping_method = form.cleaned_data.get("shipping_method")
        email = form.cleaned_data.get("email")
        order_notes = form.cleaned_data.get("order_notes")

        order = self.create_order(
            address=new_address,
            email=email,
            shipping_method=shipping_method,
            order_notes=order_notes,
        )

        self.create_order_items_from_cart(order)

        url = reverse_lazy("stripe-view", args=[order.id])
        return HttpResponseRedirect(url)

    def get_initial(
        self, *args: tuple[Any], **kwargs: dict[str, Any]
    ) -> dict[str, Any]:
        initial: dict[str, Any] = super().get_initial()

        if self.request.user.is_authenticated and not self.request.user.is_anonymous:
            initial = self._populate_user_data(initial)

        return initial

    def dispatch(
        self, *args: tuple[Any], **kwargs: dict[str, Any]
    ) -> (
        HttpResponseRedirect
        | Coroutine[Any, Any, HttpResponseNotAllowed]
        | HttpResponseNotAllowed
    ):
        cart = Cart(self.request)
        if not cart:
            messages.error(self.request, "Your cart is empty.")
            return redirect("home-view")
        return super().dispatch(self.request, *args, **kwargs)


class OrderHistoryView(LoginRequiredMixin, FilterView, ListView):
    template_name = "orders/order_history.html"
    model = Order
    filterset_class = OrderFilter
    context_object_name = "orders"
    ordering = "-created_at"
    paginate_by = 20

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()

        queryset = queryset.filter(customer=self.request.user).prefetch_related(
            "order_items"
        )

        return queryset

    def get_context_data(
        self, *, object_list: Any = None, **kwargs: Any
    ) -> dict[str, Any]:
        context_data: dict[str, Any] = super().get_context_data(**kwargs)

        return context_data


class OrderDetailView(LoginRequiredMixin, DetailView):
    template_name = "orders/order_details.html"
    queryset = Order.objects.select_related("address").select_related("shipping_method")
    context_object_name = "order"

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(customer=self.request.user)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context_data: dict[str, Any] = super().get_context_data(**kwargs)

        context_data["items"] = OrderItem.objects.filter(
            order=context_data["order"]
        ).select_related("product")

        context_data["main_images"] = ProductImage.objects.filter(is_main_photo=True)

        context_data["payment"] = Payment.objects.get(order=context_data["order"])

        return context_data
