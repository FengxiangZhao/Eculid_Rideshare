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

    # FIXME: on debug mode, allow any emails
    if settings.DEBUG is True:
        return True

    if not CASE_ID_PATTERN.match(case_id) or domain not in CASE_EMAIL_DOMAIN:
        return False
    return True