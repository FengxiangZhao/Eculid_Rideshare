# django
from django.db import models
from django.conf import settings

class AbstractSchedule(models.Model):
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
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    scheduled_departure_datetime = models.DateTimeField()
    scheduled_departure_time_range_in_minute = models.PositiveSmallIntegerField()

    class Meta:
        abstract = True


class DriverSchedule(AbstractSchedule):
    '''
    A database model that represents the driver's schedule, extends AbstractSchedule
        car_capacity: the capacity of the car of the driver
        driver_time_constraint_in_minute: A small integer indicates how long does the driver would like to spend sending the rider
        owner: A foreign key points to the driver who created this schedule
    '''
    car_capacity = models.PositiveSmallIntegerField()
    driver_time_constraint_in_minute = models.PositiveSmallIntegerField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='driver_posts', on_delete=models.CASCADE)


class RiderSchedule(AbstractSchedule):
    '''
    A database model that represents the rider's schedule, extends AbstractSchedule

    Attributes:
        owner: A foreign key points to the rider who created this schedule
        matching_driver: A foreign key points to the driver schedule that is matched with this rider's schedule

    '''
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rider_posts', on_delete=models.CASCADE)
    matching_driver = models.ForeignKey(DriverSchedule, related_name='matched_rider', on_delete=models.CASCADE)

