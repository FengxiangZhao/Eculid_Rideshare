# django
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
# local
from .settings import EUCLID_SCHEDULE_SETTINGS
from fcm_django.models import FCMDevice


class BaseSchedule(models.Model):
    ''' A abstract database model that represents a general schedule in Rideshare App

    Attributes:
        origin: A point field stores the coordinates of the driver's start
        destination:  A point field stores the coordinates of the driver's end
        created_time: A datetime field indicates when is this schedule created
        modified_time: A datetime field indicates when is this schedule modified
        scheduled_departure_datetime: A datetime field indicates when driver would like to departure
        scheduled_departure_time_range_in_minute: A small integer indicates the range of from the scheduled_departure_datetime that driver
            would like to departure
    '''
    origin_lon = models.DecimalField(max_digits=11, decimal_places=8)
    origin_lat = models.DecimalField(max_digits=10, decimal_places=8)
    destination_lon = models.DecimalField(max_digits=11, decimal_places=8)
    destination_lat = models.DecimalField(max_digits=10, decimal_places=8)
    created_time = models.DateTimeField(verbose_name=_("Date created"), auto_now_add=True)
    modified_time = models.DateTimeField(verbose_name=_("Date modified"), auto_now=True)
    scheduled_departure_datetime = models.DateTimeField(_("Scheduled departure time"))
    scheduled_departure_time_range_in_minute = models.PositiveSmallIntegerField(_("Scheduled departure time range (minute)"))
    latest_arrival_datetime = models.DateField(_('The latest time to arrive at destination'), blank=True)
    estimated_route_time_in_minute = models.PositiveSmallIntegerField(_("The estimated time for the trip"))
    is_cancelled = models.BooleanField(verbose_name=_("The schedule is cancelled or not."), default=False)
    owner = models.ForeignKey(EUCLID_SCHEDULE_SETTINGS["AUTH_USER_MODEL"], on_delete=models.CASCADE)

    @property
    def is_active(self):
        '''
        :return: True if the schedule is active
        '''
        time_based_is_active = timezone.now() + EUCLID_SCHEDULE_SETTINGS.LEAD_CUTOFF_TIME < self.scheduled_departure_datetime
        return time_based_is_active and not self.is_cancelled

    @property
    def origin_latlon(self):
        '''
        :return: A tuple contains the lat/lon of the origin
        '''
        return (self.origin_lat, self.origin_lon)

    @property
    def dest_latlon(self):
        '''
        :return: A tuple contains the lat/lon of the destination
        '''
        return (self.destination_lat, self.destination_lon)

    def get_latlons(self):
        '''
        Obtains the latitude and longitude of the origin and destination
        :return: two lon/lat pairs for origin and destination
        '''
        return self.origin_latlon, self.dest_latlon

    def get_departure_time_window(self) -> (timezone.datetime,):
        '''
        Obtains the departure time window
        :return: a tuple represents the departure timewindow
        '''
        return self.scheduled_departure_datetime, self.scheduled_departure_datetime + timezone.timedelta(minutes=self.scheduled_departure_time_range_in_minute)

    def get_arrival_time_window(self) -> (timezone.datetime,):
        '''
        Obtains the arrival time window
        :return:
        '''
        return self.latest_arrival_time - timezone.timedelta(self.scheduled_departure_time_range_in_minute), self.latest_arrival_time

    def save(self, *args, **kwargs):
        '''
        Overwrite the save method
        '''
        self.latest_arrival_time = self.scheduled_departure_datetime + timezone.timedelta(minutes=self.estimated_route_time_in_minute +
                                                                                                  self.scheduled_departure_time_range_in_minute)
        super(BaseSchedule, self).save(*args, **kwargs)

    def cancel(self):
        '''
        The owner of the object actively executes the cancellation
        Not implemented on the base class
        '''
        return NotImplementedError("Base class method does not have implementation")

    def notify_user(self, template_name, context):
        '''
        Notify user through email and push notifications
        Cancellation context should have { username, reason, result }
        Matched context should have { username , }
        :param template_name: the template to be used
        :param context: the context for the template
        '''
        templates_attr = {
            "cancellation" : {
                "template_location" : "api",
                "template_prefix" : "cancellation",
            },
            "matched": {
                "template_location": "api",
                "template_prefix": "matched",
            },
        }

        from euclid_verification.tasks import send_email_with_template_task, send_fcm_text_message_with_template_task
        send_email_with_template_task(**templates_attr.get(template_name), context=context, email=self.owner.email)
        device = FCMDevice.objects.get(user=self.owner, active=True)
        send_fcm_text_message_with_template_task(**templates_attr.get(template_name), context=context, device_id=device.device_id)

    def __str__(self):
        return "Trip No.{:d} scheduled at {:s} from {:s} to {:s}".format(
            self.id,
            "({:8f}, {:8f})".format(self.origin_lon, self.origin_lat),
            "({:8f}, {:8f})".format(self.destination_lon, self.destination_lat),
            self.scheduled_departure_datetime.strftime("%Y-%m-%d %H:%M:%S")
        )

    class Meta:
        abstract = True



class DriverSchedule(BaseSchedule):
    '''
    A database model that represents the driver's schedule, extends AbstractSchedule
        car_capacity: the capacity of the car of the driver
        driver_time_constraint_in_minute: A small integer indicates how long does the driver would like to spend sending the rider
        owner: A foreign key points to the driver who created this schedule
    '''
    car_capacity = models.PositiveSmallIntegerField(_("Car capacity of the driver."))
    driver_time_constraint_in_minute = models.PositiveSmallIntegerField()

    @property
    def has_match(self):
        return RiderSchedule.objects.filter(matching_driver=self).exists()

    def get_arrival_time_window(self) -> (timezone.datetime,):
        '''
        Obtains the arrival time window
        '''
        return (self.latest_arrival_time - timezone.timedelta(self.scheduled_departure_time_range_in_minute + self.driver_time_constraint_in_minute),
                self.latest_arrival_time)

    def save(self, *args, **kwargs):
        '''
        Overwrite the save method
        '''
        self.latest_arrival_time = self.scheduled_departure_datetime + timezone.timedelta(minutes=self.estimated_route_time_in_minute +
                                                                                                  self.scheduled_departure_time_range_in_minute +
                                                                                                  self.driver_time_constraint_in_minute)
        super(BaseSchedule, self).save(*args, **kwargs)


class RiderSchedule(BaseSchedule):
    '''
    A database model that represents the rider's schedule, extends AbstractSchedule

    Attributes:
        owner: A foreign key points to the rider who created this schedule
        matching_driver: A foreign key points to the driver schedule that is matched with this rider's schedule

    '''
    matching_driver = models.ForeignKey(DriverSchedule, on_delete=models.CASCADE, blank=True, null=True)

    @property
    def has_match(self):
        return self.matching_driver is not None

    def set_matching_driver(self, driver):
        '''
        Set the matching driver, meaning that this rider is successfully paired with a driver, and send notifications
        '''
        if not self.matching_driver:
            self.matching_driver = driver
            # TODO: figure out ways to perform match
            self.notify_user("matched", {})
            self.save()