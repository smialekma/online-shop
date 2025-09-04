from typing import List

import stripe
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from orders.models import Order
from payments.models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


def _create_line_items(order: Order) -> List[dict]:
    line_items = []

    for order_item in order.order_items.all():
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


def _create_shipping_option(order: Order) -> List[dict]:
    method = order.shipping_method

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


def _create_new_payment(session_object, order: Order):
    amount = session_object.amount_total / 100

    Payment.objects.create(
        stripe_checkout_id=session_object.id,
        order=order,
        amount=amount,
        status="unpaid",
    )


def create_checkout_session(request, order_id):
    print(order_id)
    print(request.POST)

    order = (
        Order.objects.prefetch_related("order_items")
        .select_related("shipping_method")
        .get(id=order_id)
    )

    line_items = _create_line_items(order)

    shipping_option = _create_shipping_option(order)

    session = stripe.checkout.Session.create(
        shipping_options=shipping_option,
        customer_email=request.user.email if request.user.is_authenticated else None,
        line_items=line_items,
        mode="payment",
        success_url=request.build_absolute_uri(reverse_lazy("stripe-success-view")),
        cancel_url=request.build_absolute_uri(reverse_lazy("stripe-cancel-view")),
    )

    # create new payment object
    _create_new_payment(session, order)

    return redirect(session.url, code=303)


@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = request.body
    event = None
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except stripe.error.SignatureVerificationError as e:
        print("⚠️  Webhook signature verification failed." + str(e))
        return HttpResponse(status=400)

    # Handle the event
    if event.type == "checkout.session.completed":
        session = event.data.object
        checkout_session_id = session.get("id")
        _handle_checkout_session_completed(checkout_session_id)
    else:
        print("Unhandled event type {}".format(event.type))

    return HttpResponse(status=200)


def _handle_checkout_session_completed(checkout_session_id):
    payment = Payment.objects.select_related("order").get(
        stripe_checkout_id=checkout_session_id
    )
    payment.status = "paid"
    payment.order.is_paid = True
    payment.order.save()
    payment.save()


def success(request):
    return render(request, "payments/success.html")


def cancel(request):
    return render(request, "payments/cancel.html")
