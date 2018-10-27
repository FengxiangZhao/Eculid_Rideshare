# django
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
# local
from .verifications import validate_case_email


class ClientManager(BaseUserManager):
    '''
    A basic client manager
    '''
    def create_user(self, username, email, password, phone):
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
    '''
    A basic client model
    '''
    username = models.CharField(max_length=100, unique=True, db_index=True)
    pwd = models.CharField(max_length=128)
    phone = models.CharField(max_length=20, unique=True)
    email = models.CharField(max_length=254, unique=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    is_email_verified = models.BooleanField("email verification status", default=False,
                                            help_text="user must verify the email to use the API")
    is_staff = models.BooleanField('staff status', default=False,
                                   help_text='flag for log into admin site.')
    is_active = models.BooleanField('active', default=True)
    is_superuser = models.BooleanField('superuser', default=False)

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