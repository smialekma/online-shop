from typing import cast

import stripe
from django.http import HttpResponse, HttpRequest
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from stripe.checkout import Session
from django.core.mail import EmailMessage
from django.db import transaction
from django.db.models import F
from stripe.params.checkout import (
    SessionCreateParamsShippingOption,
    SessionCreateParamsLineItem,
)

from core import settings
from orders.models import Order
from payments.models import Payment


class StripePaymentProvider:

    def __init__(self, request: HttpRequest, order_id: int | None = None) -> None:
        self.order_id = order_id
        self.request = request

        if order_id:
            order = self._get_order()
            self.order = order

    def _get_order(self) -> Order:
        order: Order = (
            Order.objects.prefetch_related("order_items")
            .select_related("shipping_method")
            .get(id=self.order_id)
        )
        return order

    def _create_line_items(self) -> list[SessionCreateParamsLineItem]:
        line_items = []

        for order_item in self.order.order_items.all():
            product = order_item.product

            line_items.append(
                {
                    "price_data": {
                        "currency": "pln",
                        "product_data": {
                            "name": product.name,
                        },
                        "unit_amount": int(product.price * 100),
                    },
                    "quantity": order_item.quantity,
                }
            )

        return cast(list[SessionCreateParamsLineItem], line_items)

    def _create_shipping_option(self) -> list[SessionCreateParamsShippingOption]:
        method = self.order.shipping_method

        order_amount = int(method.price * 100)
        display_name = method.name
        min_delivery = method.min_delivery_time_in_days
        max_delivery = method.max_delivery_time_in_days

        shipping_options = [
            {
                "shipping_rate_data": {
                    "type": "fixed_amount",
                    "fixed_amount": {"amount": order_amount, "currency": "pln"},
                    "display_name": display_name,
                    "delivery_estimate": {
                        "minimum": {"unit": "business_day", "value": min_delivery},
                        "maximum": {"unit": "business_day", "value": max_delivery},
                    },
                },
            },
        ]

        return cast(list[SessionCreateParamsShippingOption], shipping_options)

    def _create_new_payment(self, session_object: Session) -> None:
        if session_object.amount_total:
            amount = int(session_object.amount_total) / 100

            Payment.objects.create(
                stripe_checkout_id=session_object.id,
                order=self.order,
                amount=amount,
                is_paid=False,
            )
        else:
            raise TypeError("Session_object.amount_total is None, but should be int")

    def _handle_payment_intent_succeeded(
        self, payment_intent_id: str, payment: Payment
    ) -> None:
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        payment_method_id = payment_intent.payment_method

        if payment_method_id is str:
            payment_method_id_str: str = str(payment_method_id)
            payment_method = stripe.PaymentMethod.retrieve(payment_method_id_str)
            payment_method_type = payment_method.get("type")
            payment.payment_method = payment_method_type
            payment.save()
        else:
            raise TypeError(
                "Retrieved variable is of incorrect type: payment_method_id"
            )

    def _handle_checkout_session_completed(
        self, checkout_session_id: str, username: str
    ) -> Payment:
        with transaction.atomic():
            payment: Payment = (
                Payment.objects.select_related("order")
                .prefetch_related("order__order_items")
                .prefetch_related("order__order_items__product")
                .get(stripe_checkout_id=checkout_session_id)
            )
            payment.is_paid = True
            payment.save()

            for item in payment.order.order_items.all():
                item.product.quantity = F("quantity") - item.quantity
                item.product.save(updated_fields=["quantity"])

        self.order_id = payment.order.pk
        email = payment.order.email

        self._send_email(email, username)

        return payment

    def create_checkout_session(self) -> str | None:
        line_items = self._create_line_items()

        shipping_option = self._create_shipping_option()

        session = stripe.checkout.Session.create(
            shipping_options=shipping_option,
            customer_email=(
                self.request.user.email if self.request.user.is_authenticated else ""
            ),
            line_items=line_items,
            mode="payment",
            success_url=self.request.build_absolute_uri(
                reverse_lazy("stripe-success-view")
            ),
            cancel_url=self.request.build_absolute_uri(
                reverse_lazy("stripe-cancel-view")
            ),
            metadata={
                "username": (
                    self.request.user.username
                    if self.request.user.is_authenticated
                    else ""
                )
            },
        )

        # create new payment object
        self._create_new_payment(session)

        return session.url

    def handle_webhook(self) -> HttpResponse:
        payload = self.request.body
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
        sig_header = self.request.headers.get("stripe-signature")

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except stripe.SignatureVerificationError:
            return HttpResponse(status=400)

        # Handle the event
        if event.type == "checkout.session.completed":
            session = event.data.object
            checkout_session_id = session.get("id")
            username = session.get("metadata", {}).get("username")

            payment = self._handle_checkout_session_completed(
                checkout_session_id, username=username
            )

            payment_intent_id = session.get("payment_intent")
            self._handle_payment_intent_succeeded(payment_intent_id, payment)

        else:
            raise Exception("Unhandled event type {}".format(event.type))

        return HttpResponse(status=200)

    def _send_email(self, to_email: str, username: str) -> None:

        mail_subject = "Online Shop - you have placed an order"
        message = render_to_string(
            "payments/success_email.html",
            {
                "order_id": self.order_id,
                "username": (username if username else to_email),
            },
        )
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
