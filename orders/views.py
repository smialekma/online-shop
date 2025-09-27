from decimal import Decimal
from typing import Optional

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from django_filters.views import FilterView

from carts.cart import Cart
from customer_addresses.forms import AddressForm
from customer_addresses.models import CustomerAddress
from customers.views import CustomLoginView
from orders.filters import OrderFilter
from orders.models import Order, OrderItem, ShippingMethod
from django.http import HttpResponseRedirect

from payments.models import Payment
from products.models import ProductImage


class CheckoutLoginView(CustomLoginView):
    template_name = "orders/checkout_login.html"
    next_page = reverse_lazy("checkout-view")
    redirect_authenticated_user = True


class CheckoutView(CreateView):
    form_class = AddressForm
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
        order_total_price: Decimal = cart_total_price + shipping_method.price

        order = Order.objects.create(
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
                product=cart_item["product"],
                quantity=cart_item["quantity"],
            )
        cart.clear()

    @transaction.atomic
    def form_valid(self, form):
        new_address = form.save(commit=False)

        address_dct = {
            "first_name": new_address.first_name,
            "last_name": new_address.last_name,
            "address_line": new_address.address_line,
            "telephone": new_address.telephone,
            "postal_code": new_address.postal_code,
            "city": new_address.city,
            "country": new_address.country,
        }

        if self.request.user.is_authenticated:
            new_address = CustomerAddress.objects.update_or_create(
                defaults=address_dct, customer=self.request.user
            )[0]

        else:
            new_address = CustomerAddress.objects.create(**address_dct, customer=None)

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

        self.object = new_address
        url = reverse_lazy("stripe-view", args=[order.id])
        return HttpResponseRedirect(url)

    def get_initial(self, *args, **kwargs):
        initial = super().get_initial()

        if self.request.user.is_authenticated and not self.request.user.is_anonymous:
            initial = self._populate_user_data(initial)

        return initial

    def _get_address_or_none(self, user) -> CustomerAddress | None:
        try:
            address = (
                CustomerAddress.objects.filter(customer=user).order_by("-id").last()
            )
        except CustomerAddress.DoesNotExist:
            address = None

        return address

    def _populate_user_data(self, initial):
        initial["email"] = self.request.user.email

        address = self._get_address_or_none(self.request.user)

        if address:
            initial = self._populate_address_data(initial, address)

        return initial

    def _populate_address_data(self, initial, address):
        address_fields = [
            "first_name",
            "last_name",
            "address_line",
            "telephone",
            "postal_code",
            "city",
            "country",
        ]

        for field in address_fields:
            if hasattr(address, field):
                initial[field] = getattr(address, field)

        return initial

    def dispatch(self, request, *args, **kwargs):
        cart = request.session.get("cart", {})
        if not cart:
            messages.error(request, "Your cart is empty.")
            return redirect("home-view")
        return super().dispatch(request, *args, **kwargs)


class OrderHistoryView(LoginRequiredMixin, FilterView, ListView):
    template_name = "orders/order_history.html"
    model = Order
    filterset_class = OrderFilter
    context_object_name = "orders"
    ordering = "-created_at"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.filter(customer=self.request.user).prefetch_related(
            "order_items"
        )

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)

        print(context_data)

        return context_data


class OrderDetailView(LoginRequiredMixin, DetailView):
    template_name = "orders/order_details.html"
    queryset = Order.objects.select_related("address").select_related("shipping_method")
    context_object_name = "order"

    def get_queryset(self):
        return super().get_queryset().filter(customer=self.request.user)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data["items"] = OrderItem.objects.filter(
            order=context_data["order"]
        ).select_related("product")

        context_data["main_images"] = ProductImage.objects.filter(is_main_photo=True)

        payment = Payment.objects.get(order=context_data["order"])
        print(payment.id)
        print(payment.payment_method)

        context_data["payment"] = Payment.objects.get(order=context_data["order"])

        return context_data
