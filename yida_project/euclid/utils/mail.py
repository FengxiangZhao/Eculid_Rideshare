import os

from django.conf import settings

from django.core.mail import EmailMessage, EmailMultiAlternatives

from django.template.loader import render_to_string

from utils.template import load_template_to_string


def send_email_with_template(template_location, template_prefix, context, recipient):
    '''
    Send an email based on the template given
    The template should be placed under `<PROJECT>/templates/<APP_NAME>`
    The name of the template should be `email_<template_prefix>_[subject | body].txt`
    Current method only supports plain text
    Args:
        template_prefix: the prefix of the template
        template_location: the location of the template
        recipient: the email to be sent to, could be a single string or a list of string
    '''
    # subject_template_location = os.path.join(template_location, "email_%s_subject.txt") % template_prefix
    # body_template_location    = os.path.join(template_location, "email_%s_body.txt")    % template_prefix
    #
    # subject = render_to_string(subject_template_location, context=context)
    # body = render_to_string(body_template_location, context=context)

    subject = load_template_to_string(template_location, "email_{:s}_subject.txt".format(template_prefix), context)
    body = load_template_to_string(template_location, "email_{:s}_body.txt".format(template_prefix), context)

    send_email(subject, body, recipient)

def send_html_email_with_template(template_location, template_prefix, context, recipient):
    # subject_template_location = os.path.join(template_location, "email_%s_subject.txt") % template_prefix
    # body_template_location    = os.path.join(template_location, "email_%s_body.txt")    % template_prefix
    # html_template_location    = os.path.join(template_location, "email_%s_body.html")   % template_prefix
    # html = render_to_string(html_template_location, context=context)

    subject = load_template_to_string(template_location, "email_{:s}_subject.txt".format(template_prefix), context)
    body = load_template_to_string(template_location, "email_{:s}_body.txt".format(template_prefix), context)
    html = load_template_to_string(template_location, "email_{:s}_body.html".format(template_prefix), context)

    send_html_email(subject, body, html, recipient)

def send_email(subject, body, recipient):
    # Avoid header injection
    subject = ''.join(subject.splitlines())
    if type(recipient) is list:
        msg = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, recipient)
    else:
        msg = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, [recipient])
    msg.send(fail_silently=False)

def send_html_email(subject, body, html, recipient):
    subject = ''.join(subject.splitlines())
    if type(recipient) is list:
        msg = EmailMultiAlternatives(subject, body, settings.DEFAULT_FROM_EMAIL, recipient)
    else:
        msg = EmailMultiAlternatives(subject, body, settings.DEFAULT_FROM_EMAIL, [recipient])
    msg.attach_alternative(html, "text/html")
    msg.send(fail_silently=False)

