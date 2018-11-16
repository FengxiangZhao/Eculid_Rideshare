from celery import shared_task
from .mail import send_email_with_template

@shared_task
def send_email_with_template_task(template_location, template_prefix, context, recipient):
    send_email_with_template(template_location, template_prefix, context, recipient)