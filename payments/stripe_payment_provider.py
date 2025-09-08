from typing import List

import stripe
from django.http import HttpResponse
from django.urls import reverse_lazy
from stripe.checkout import Session

from core import settings
from orders.models import Order
from payments.models import Payment


class StripePaymentProvider:

    def __init__(self, request, order_id=None):
        self.order_id = order_id
        self.request = request

        if order_id:
            order = self._get_order()
            self.order = order

    def _get_order(self) -> Order:
        order = (
            Order.objects.prefetch_related("order_items")
            .select_related("shipping_method")
            .get(id=self.order_id)
        )
        return order

    def _create_line_items(self) -> List[dict]:
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

        return line_items

    def _create_shipping_option(self) -> List[dict]:
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

        return shipping_options

    def _create_new_payment(self, session_object: Session) -> None:
        amount = session_object.amount_total / 100

        Payment.objects.create(
            stripe_checkout_id=session_object.id,
            order=self.order,
            amount=amount,
            is_paid=False,
        )

    def _handle_payment_intent_succeeded(
        self, payment_intent_id: str, payment: Payment
    ) -> None:
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        payment_method_id = payment_intent.payment_method
        payment_method = stripe.PaymentMethod.retrieve(payment_method_id)
        payment_method_type = payment_method.get("type")
        payment.payment_method = payment_method_type
        payment.save()

    def _handle_checkout_session_completed(self, checkout_session_id: str) -> Payment:
        payment = Payment.objects.select_related("order").get(
            stripe_checkout_id=checkout_session_id
        )
        payment.is_paid = True
        payment.save()

        return payment

    def create_checkout_session(self) -> str:
        line_items = self._create_line_items()

        shipping_option = self._create_shipping_option()

        session = stripe.checkout.Session.create(
            shipping_options=shipping_option,
            customer_email=(
                self.request.user.email if self.request.user.is_authenticated else None
            ),
            line_items=line_items,
            mode="payment",
            success_url=self.request.build_absolute_uri(
                reverse_lazy("stripe-success-view")
            ),
            cancel_url=self.request.build_absolute_uri(
                reverse_lazy("stripe-cancel-view")
            ),
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
        except stripe.error.SignatureVerificationError as e:
            print("⚠️  Webhook signature verification failed." + str(e))
            return HttpResponse(status=400)

        # Handle the event
        if event.type == "checkout.session.completed":
            session = event.data.object
            checkout_session_id = session.get("id")
            payment = self._handle_checkout_session_completed(checkout_session_id)

            payment_intent_id = session.get("payment_intent")
            self._handle_payment_intent_succeeded(payment_intent_id, payment)

        else:
            print("Unhandled event type {}".format(event.type))

        return HttpResponse(status=200)
