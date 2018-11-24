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
    estimated_route_time_in_minute = models.PositiveIntegerField(verbose_name=_("Estimated time on route (minute)"))
    is_cancelled = models.BooleanField(verbose_name=_("The schedule is cancelled or not."), default=True)

    @property
    def is_active(self):
        time_based_is_active = timezone.now() + EUCLID_SCHEDULE_SETTINGS.LEAD_CUTOFF_TIME < self.scheduled_departure_datetime
        return time_based_is_active and not self.is_cancelled

    class Meta:
        abstract = True

    @property
    def earliest_departure_time(self):
        return self.scheduled_departure_datetime

    @property
    def latest_arrival_time(self):
        return self.scheduled_departure_datetime + timezone.timedelta(minutes=self.estimated_route_time_in_minute)

    def _cancel(self):
        if not self.is_cancelled:
            self.is_cancelled = True
            self._notify_owner()
            self.save()

    def _notify_owner(self, **context):
        return NotImplementedError("Base schedule does not offer functionalities of notifying user")




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
    def latest_arrival_time(self):
        return super(DriverSchedule, self).latest_arrival_time + timezone.timedelta(minutes=self.driver_time_constraint_in_minute)

    @property
    def has_match(self):
        return RiderSchedule.objects.filter(matching_driver=self).exists()




class RiderSchedule(BaseSchedule):
    '''
    A database model that represents the rider's schedule, extends AbstractSchedule

    Attributes:
        owner: A foreign key points to the rider who created this schedule
        matching_driver: A foreign key points to the driver schedule that is matched with this rider's schedule

    '''
    owner = models.ForeignKey(EUCLID_SCHEDULE_SETTINGS["AUTH_USER_MODEL"], related_name='rider_posts', on_delete=models.CASCADE)
    matching_driver = models.ForeignKey(DriverSchedule, on_delete=models.CASCADE, blank=True, null=True)

    @property
    def has_match(self):
        return self.matching_driver is not None

