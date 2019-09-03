from celery import shared_task
from django.conf import settings
from utils.mail import send_email_with_template
from fcm_django.models import FCMDevice
from utils.template import load_fcm_text_message_from_template


@shared_task
def send_email_with_template_task(template_location, template_prefix, context, email):
    send_email_with_template(template_location, template_prefix, context, email)

@shared_task
def send_fcm_text_message_with_template_task(template_location, template_prefix, context, device_id):
    device = FCMDevice.objects.get(device_id=device_id)
    title, body = load_fcm_text_message_from_template(template_location, template_prefix, context)
    device.send_message(title=title, body=body, api_key=getattr(settings, ""))
