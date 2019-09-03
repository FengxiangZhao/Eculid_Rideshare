# package
import uuid
# django
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
# local
from .exceptions import EmailVerificationTokenExpired, EmailVerificationTokenInvalid


# Create your models here.


def _get_verification_token():
    """
    obtain a verification token.
    Returns: a alphanumeric token with length of 32
    """
    return uuid.uuid4().hex


class AbstractBaseToken(models.Model):
    '''
    An abstract database models to store char tokens.
    Token is in the form of hexadecimal numbers with a maximal length of 128
    '''
    token = models.CharField(_("token"), max_length=128, unique=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.token


class EmailVerificationTokenManager(models.Manager):
    '''
    A database model manager for EmailVerificationToken that provides utilities to manage the tokens
    '''
    def create_email_verification_token(self, client, save=True):
        '''
        Create a email verification token
        Args:
            client: the client associated with the token
            save: arguments for saving the token on create or not

        Returns: the token instance created
        '''
        token = self.model(
            client=client,
            token=_get_verification_token()
        )
        if save:
            token.save()
        return token

    def reset_email_verification_token(self, old_client_token):
        '''
        Reset the email verification token
        If the old token is expired and the client associated with this token is not verified
            at the time of the method call, the token should be reassigned.
        On other cases, the original token will be returned, if it exists in the database.
        This handles the case the is_expired returns false when the user is verified.

        Args:
            old_client_token: the old hexadecimal token that is expired

        Returns: The token instance related to the user

        Raises:
            EmailVerificationTokenInvalid: if the token does not exist in the database
        '''
        try:
            old_token = self.model.objects.get(token=old_client_token)
        except self.model.DoesNotExist:
            raise EmailVerificationTokenInvalid

        if not old_token.is_verified and old_token.is_expired:
            old_token.delete()
            return self.create_email_verification_token(old_token.client, save=True)
        return old_token

    def verify_client(self, client_token):
        '''
        Verify the client related to the token

        Args:
            client_token: the hexadecimal token related to the user

        Raises:
            EmailVerificationTokenInvalid: if the token provided is not associated with any token
            EmailVerificationTokenExpired: if the token provided related to a client that is already activated or the token is expired
        '''
        try:
            token = self.model.objects.get(token=client_token)
        except self.model.DoesNotExist:
            raise EmailVerificationTokenInvalid
        if not token.is_expired:
            # mark the token is verified
            token.verified_time = timezone.now()
            token.save()
            # mark the client is verified
            token.client.is_email_verified = True
            token.client.save()
        else:
            raise EmailVerificationTokenExpired
        return True

class EmailVerificationToken(AbstractBaseToken):
    '''
    An database model for the email verification token.
    Contains reference to the original client and the functionalities for verification and send email
    '''
    verified_time = models.DateTimeField(blank=True, null=True)
    client = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name="email_verification_token",
                               on_delete=models.CASCADE)

    objects = EmailVerificationTokenManager()

    def send_verification_email(self):
        '''
        Send an verification email
        '''
        context = {
            'username' : self.client.username,
            "url": settings.HOSTING_URL,
            "token": self.token
        }
        # send_html_email_with_template("api", "verification", context, self.client.email)
        from euclid_verification.tasks import send_email_with_template_task
        send_email_with_template_task.delay("api", "verification", context, self.client.email)

    @property
    def is_verified(self):
        '''
        A property that checks if the email address is marked confirmed
        Returns: true if the email address is confirmed
        '''
        return not self.verified_time is None

    @property
    def token_expiration_time(self):
        '''
        The time that the token will be expired
        When `EMAIL_CONFIRMATION_PERIOD' is not set, the return value will be None

        Returns: a datetime object represent when will the token expire
        '''
        period = getattr(settings, 'EMAIL_CONFIRMATION_PERIOD', None)
        if period is None:
            return None
        return self.created_time + period

    @property
    def is_expired(self):
        '''
        Check whether the token is expired.
        A token is expired if the time constraint is passed or the user is already verified
            note: Token expired page provides mechanism for update the token that will send new link to the user.
            note: Do not update the token and send email if the user is verified
        When `EMAIL_CONFIRMATION_PERIOD' is not set, the token will never expire

        Returns: True if the token is expired, false otherwise

        '''
        period = getattr(settings, 'EMAIL_CONFIRMATION_PERIOD', None)
        if self.is_verified:
            return True
        else:
            expiration_time = self.token_expiration_time
            if expiration_time is None:
                return False
            return timezone.now() > expiration_time

