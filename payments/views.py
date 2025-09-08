import stripe
from django.conf import settings
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from payments.stripe_payment_provider import StripePaymentProvider

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(request, order_id):
    payment_provider = StripePaymentProvider(request, order_id)

    session_url = payment_provider.create_checkout_session()

    return redirect(session_url, code=303)


@csrf_exempt
@require_POST
def stripe_webhook(request):
    payment_provider = StripePaymentProvider(request)
    return payment_provider.handle_webhook()


def success(request):
    return render(request, "payments/success.html")


def cancel(request):
    return render(request, "payments/cancel.html")
