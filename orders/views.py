from decimal import Decimal
from typing import Optional

from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from carts.cart import Cart
from customer_addresses.forms import AddressForm
from customer_addresses.models import CustomerAddress
from customers.views import CustomLoginView
from orders.models import Order, OrderItem, ShippingMethod


class CheckoutLoginView(CustomLoginView):
    template_name = "orders/checkout_login.html"
    next_page = reverse_lazy("checkout-view")
    redirect_authenticated_user = True


class CheckoutView(CreateView):
    form_class = AddressForm
    template_name = "orders/checkout.html"
    success_url = reverse_lazy("home-view")

    def _get_address_or_none(self, user) -> CustomerAddress | None:
        try:
            address = (
                CustomerAddress.objects.filter(customer=user).order_by("-id").last()
            )
        except CustomerAddress.DoesNotExist:
            address = None

        return address

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

        if self.request.user.is_authenticated:
            new_address.customer = self.request.user

        new_address = CustomerAddress.objects.update_or_create(
            defaults=new_address.__dict__, address_line=new_address.address_line
        )[0]
        # TODO - make it work
        # - update
        # - only 1 instance (now 2 new addresses created)

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

        return super().form_valid(form)

    def get_initial(self, *args, **kwargs):
        initial = super().get_initial()

        if self.request.user.is_authenticated:
            initial["email"] = self.request.user.email

            address = self._get_address_or_none(self.request.user)

            if address:
                initial["first_name"] = address.first_name
                initial["last_name"] = address.last_name
                initial["address_line"] = address.address_line
                initial["telephone"] = address.telephone
                initial["postal_code"] = address.postal_code
                initial["city"] = address.city
                initial["country"] = address.country

        return initial

    def dispatch(self, request, *args, **kwargs):
        cart = request.session.get("cart", {})
        if not cart:
            messages.error(request, "Your cart is empty.")
            return redirect("home-view")
        return super().dispatch(request, *args, **kwargs)
