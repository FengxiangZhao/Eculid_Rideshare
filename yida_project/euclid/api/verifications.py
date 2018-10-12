import re

import os

import uuid

from django.conf import settings

from django.core.mail import EmailMessage

from django.template import loader


# A Case ID pattern, recoginizes lower-case alphanumeric in the form <Three letter><1-9999>
CASE_ID_PATTERN = re.compile(r"^[a-z]{3}((?!0))[0-9]{1,4}$")
# A list contains all recognized case email domain
# Currently, since CWRU offers alias, only should <case id>@case.edu should be allowed
CASE_EMAIL_DOMAIN = ["case.edu",]

# Usage: CASE_ID_PATTERN.match(case_id)

def validate_case_email(email):
    '''
    Use regular expression to validate the given email address
    Args:
        email: the address provided

    Returns: True if the provided email address is a valid case email address,
        False otherwise
    '''

    try:
        case_id, domain = email.split("@")
    except ValueError as e:
        return False

    if not CASE_ID_PATTERN.match(case_id) or not email in CASE_EMAIL_DOMAIN:
        return False
    return True

########################################################

def sent_email_with_template(template_location, template_prefix, context, recipient):
    '''
    Send an email based on the template given
    The template should be placed under `<PROJECT>/templates/<APP_NAME>`
    The name of the template should be `email_<template_prefix>_[subject | body].txt`
    Current method only supports plain text
    Args:
        template_prefix: the prefix of the template
        template_location: the location of the template
        recipient: the email to be sent to
    '''
    subject_template_location = os.path.join(template_location, "email_%s_subject.txt") % template_prefix
    body_template_location    = os.path.join(template_location, "email_%s_body.txt")    % template_prefix

    subject = load_template(subject_template_location, context)
    body = load_template(body_template_location, context)

    send_email(subject, body, recipient)


def load_template(template_name, context):
    '''
    Generate String based on template and context
    Args:
        template_name: the uri to the template
        context: the context to be passed into the template

    Returns: a String of the rendered message

    '''
    return loader.render_to_string(template_name, context=context)


def send_email(subject, body, recipient):
    # Avoid header injection
    subject = ''.join(subject.splitlines())
    msg = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, [recipient])
    msg.send()


def get_verification_token():
    '''
    obtain a verification token.
    Returns: a alphanumeric token
    '''
    return uuid.uuid4().hex