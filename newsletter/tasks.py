from django.core.mail import EmailMessage

from newsletter.models import Subscriber, NewsletterPost

from celery import shared_task


@shared_task
def send_newsletter() -> None:
    active_subscribers = Subscriber.objects.filter(is_active=True)
    post_to_send = (
        NewsletterPost.objects.filter(is_published=False, to_publish=True)
        .order_by("-created_at")
        .first()
    )

    mail_subject = post_to_send.title
    message = post_to_send.body

    for subscriber in active_subscribers:
        to_email = subscriber.email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
