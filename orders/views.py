from typing import Optional

from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import CreateView

from carts.cart import Cart
from customer_addresses.forms import AddressForm
from customer_addresses.models import CustomerAddress
from orders.models import Order, OrderItem


class CheckoutView(CreateView):
    form_class = AddressForm
    template_name = "orders/checkout.html"
    success_url = reverse_lazy("home-view")

    def create_order(
        self, address: CustomerAddress, email: str, order_notes: Optional[str] = None
    ) -> Order:
        cart = Cart(self.request)
        order = Order.objects.create(
            address=address,
            total_amount=cart.get_total_price(),
            email=email,
            order_notes=order_notes,
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
        address = form.save()
        address.save()

        email = form.cleaned_data["email"]
        order_notes = form.cleaned_data["order_notes"]

        order = self.create_order(address, email, order_notes)

        self.create_order_items_from_cart(order)

        if self.request.user.is_authenticated:
            # TODO - save the address to the current user
            user = self.request.user
            user.address = address
            user.save()

        return super().form_valid(form)

    def get_initial(self, *args, **kwargs):
        initial = super().get_initial()

        if self.request.user.is_authenticated:
            initial["email"] = self.request.user.email

        return initial
