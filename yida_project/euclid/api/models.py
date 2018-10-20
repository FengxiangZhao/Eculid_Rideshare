# django
from django.db import models
from django.conf import settings
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
            username,
            email,
            phone
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
    email = models.CharField(max_length=16, unique=True)

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


class DriverSchedule(models.Model):
    ''' A database model that represents the driver's schedule

    Attributes:
        origin: A point field stores the coordinates of the driver's start
        destination:  A point field stores the coordinates of the driver's end
        created_time: A datetime field indicates when is this schedule created
        modified_time: A datetime field indicates when is this schedule modified
        scheduled_departure_datetime: A datetime field indicates when driver would like to departure
        scheduled_departure_time_range_in_minute: A small integer indicates the range of from the scheduled_departure_datetime that driver
            would like to departure
        driver_time_constraint_in_minute: A small integer indicates how long does the driver would like to spend sending the rider
        owner: A foreign key points to the user who created this schedule
    '''
    origin_lon = models.DecimalField(max_digits=11, decimal_places=8)
    origin_lat = models.DecimalField(max_digits=10, decimal_places=8)
    destination_lon = models.DecimalField(max_digits=11, decimal_places=8)
    destination_lat = models.DecimalField(max_digits=10, decimal_places=8)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    scheduled_departure_datetime = models.DateTimeField()
    scheduled_departure_time_range_in_minute = models.PositiveSmallIntegerField()
    driver_time_constraint_in_minute = models.PositiveSmallIntegerField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='driver_posts', on_delete=models.CASCADE)

    def clean(self):
        '''
        A set of custom rules to ensure the correctness of the data in the database
        '''
        if self.modified_time < self.created_time:
            raise ValidationError("An object cannot be modifed before it is created.")
        if self.scheduled_departure_datetime < self.created_time:
            raise ValidationError("The schedule will not come from the past.")


class RiderSchedule(models.Model):
    ''' A database model that represents the rider's schedule

    Attributes:
        origin: A point field stores the coordinates of the driver's start
        destination:  A point field stores the coordinates of the driver's end
        created_time: A datetime field indicates when is this schedule created
        modified_time: A datetime field indicates when is this schedule modified
        scheduled_departure_datetime: A datetime field indicates when driver would like to departure
        scheduled_departure_time_range_in_minute: A small integer indicates the range of from the scheduled_departure_datetime that driver
            would like to departure
        owner: A foreign key points to the user who created this schedule
        matching_driver: A foreign key points to the driver schedule that is matched with this rider's schedule
    '''
    origin_lon = models.DecimalField(max_digits=11, decimal_places=8)
    origin_lat = models.DecimalField(max_digits=10, decimal_places=8)
    destination_lon = models.DecimalField(max_digits=11, decimal_places=8)
    destination_lat = models.DecimalField(max_digits=10, decimal_places=8)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    scheduled_departure_datetime = models.DateTimeField()
    scheduled_departure_time_range_in_minute = models.PositiveSmallIntegerField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rider_posts', on_delete=models.CASCADE)
    matching_driver = models.ForeignKey(DriverSchedule, related_name='matched_rider',on_delete=models.CASCADE)

    def clean(self):
        '''
        A set of custom rules to ensure the correctness of the data in the database
        '''
        if self.modified_time < self.created_time:
            raise ValidationError("An object cannot be modifed before it is created.")
        if self.scheduled_departure_datetime < self.created_time:
            raise ValidationError("The schedule will not come from the past.")
