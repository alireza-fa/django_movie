from django.core.mail import send_mail

from celery import shared_task
from A.local_settings import EMAIL_HOST_USER


@shared_task
def send_mail_task(subject, body, receiver_list):
    status = send_mail(
        subject=subject, message=body,
        from_email=EMAIL_HOST_USER, recipient_list=receiver_list
    )
    return status
