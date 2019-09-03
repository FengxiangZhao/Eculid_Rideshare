# django
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

# local
from .verifications import validate_case_email


# Create your models here.
class ClientManager(BaseUserManager):

    def create_user(self, username, email, password, phone, save=True):
        if not email:
            raise ValidationError("Email address cannot be empty.")
        elif not validate_case_email(email):
            raise ValidationError("The email address provided is not a valid CWRU email address.")

        user = self.model(
            username=username,
            email=email,
            phone=phone
        )
        user.set_password(password)
        if save:
            user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, phone):
        user = self.create_user(username,
                                email,
                                password,
                                phone
                                )
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Client(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=128, unique=True, db_index=True)
    pwd = models.CharField(max_length=128)
    phone = models.CharField(max_length=10, unique=True)
    email = models.CharField(max_length=254, unique=True)
    is_email_verified = models.BooleanField(_("email verification status"), default=False,
                                            help_text="user must verify the email to use the API", editable=False)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text='flag for log into admin site.')
    is_active = models.BooleanField(_('active'), default=True)
    is_superuser = models.BooleanField(_('superuser'), default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone']
    objects = ClientManager()

    def clean_email(self, email):
        '''
        Validate the case email field when saving to database
        Args:
            email: the case email field
        '''
        if not validate_case_email(email):
            raise ValidationError("The email address provided is not a valid CWRU email address.")

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def __unicode__(self):
        return self.username
