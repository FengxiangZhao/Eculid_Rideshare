# django
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseBadRequest
# local
from .exceptions import EmailVerificationTokenExpired, EmailVerificationTokenInvalid
from .models import EmailVerificationToken


def client_email_verify(request):
    '''
    Views to verify user email by token
    '''
    user_token = request.GET.get("token", None)
    context = {
        "url" : settings.HOSTING_URL,
        "token" : user_token
    }
    # token is not included as an argument
    if not user_token:
        return render(request, 'api/verify_invalid_token.html', context)
    try:
        is_verified = EmailVerificationToken.objects.verify_client(user_token)
    except EmailVerificationTokenExpired:
        # The verification is expired
        return render(request, 'api/verify_email_expired.html', context)
    except EmailVerificationTokenInvalid:
        # The token is invalid
        return render(request, 'api/verify_invalid_token.html', context)

    if is_verified:
        # return verified
        return render(request, 'api/verify_email_successful.html', context)
    else:
        return HttpResponseBadRequest()

def client_email_reset(request):
    '''
    Views to reset the expired token
    '''
    user_token = request.GET.get("token", None)
    context = {
        "url": settings.HOSTING_URL,
        "token": user_token
    }
    if not user_token:
        return render(request, 'api/verify_invalid_token.html', context)

    try:
        token = EmailVerificationToken.objects.reset_email_verification_token(user_token)
    except EmailVerificationTokenInvalid:
        # The token is invalid
        return render(request, 'api/verify_invalid_token.html', context)

    if not token.is_verified:
        # the token is not verified and expired, resend email
        token.send_verification_email()

    return render(request, 'api/verify_email_resend.html', context)
