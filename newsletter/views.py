from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from newsletter.forms import NewsletterForm
from newsletter.models import Subscriber
from newsletter.tokens import newsletter_activation_token


def subscribe_newsletter(request):
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            subscriber = form.save()
            current_site = get_current_site(request)
            _send_email(current_site, subscriber, form.cleaned_data.get("email"))
            messages.success(
                request,
                "You have successfully subscribed! "
                "We've emailed you instructions for activating your newsletter. "
                "If an account exists with the email you entered, you should receive them shortly. "
                "If you don't receive an email, "
                "please make sure you've entered the correct email address, and check your spam folder.",
            )
        else:
            messages.error(request, form.errors)
    return redirect(request.META.get("HTTP_REFERER", "/"))


def _send_email(current_site, subscriber, email):
    mail_subject = "Online Shop - activate your newsletter subscription"
    message = render_to_string(
        "newsletter/newsletter_activation_email.html",
        {
            "subscriber": subscriber,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(subscriber.pk)),
            "token": newsletter_activation_token.make_token(subscriber),
        },
    )
    to_email = email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()


def confirm_subscription(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        subscriber = Subscriber.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Subscriber.DoesNotExist):
        subscriber = None
    if subscriber is not None and newsletter_activation_token.check_token(
        subscriber, token
    ):
        subscriber.is_active = True
        subscriber.save(update_fields=["is_active"])
        messages.success(
            request, "You have successfully activated your newsletter subscription."
        )
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect("home-view")
