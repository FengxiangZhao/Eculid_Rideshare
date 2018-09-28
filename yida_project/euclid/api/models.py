from django.db import models
from django.contrib.gis.db.models import PointField
from django.contrib.auth.models import User

class DriverSchedule(models.Model):
    ''' A database model that represents the driver's schedule

    Attributes:
        origin: A point field stores the coordinates of the driver's start
        destination:  A point field stores the coordinates of the driver's end
        created_time: A datetime field indicates when is this schedule created
        modified_time: A datetime field incates when is this schedule modified
        scheduled_departure_datetime: A datetime field indicates when driver would like to departure
        scheduled_departure_time_range_in_minute: A small integer indicates the range of from the scheduled_departure_datetime that driver
            would like to departure
        driver_time_constraint_in_minute: A small integer indicates how long does the driver would like to spend sending the rider
        owner: A foreign key points to the user who created this schedule
    '''
    origin = PointField()
    destination = PointField()
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    scheduled_departure_datetime = models.DateTimeField()
    scheduled_departure_time_range_in_minute = models.PositiveSmallIntegerField()
    driver_time_constraint_in_minute = models.PositiveSmallIntegerField()
    owner = models.ForeignKey(User, related_name='driver_posts', on_delete=models.CASCADE)

class RiderSchedule(models.Model):
    ''' A database model that represents the rider's schedule

    Attributes:
        origin: A point field stores the coordinates of the driver's start
        destination:  A point field stores the coordinates of the driver's end
        created_time: A datetime field indicates when is this schedule created
        modified_time: A datetime field incates when is this schedule modified
        scheduled_departure_datetime: A datetime field indicates when driver would like to departure
        scheduled_departure_time_range_in_minute: A small integer indicates the range of from the scheduled_departure_datetime that driver
            would like to departure
        owner: A foreign key points to the user who created this schedule
        matching_driver: A foreign key points to the driver schedule that is matched with this rider's schedule
    '''
    origin = PointField()
    destination = PointField()
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    scheduled_departure_datetime = models.DateTimeField()
    scheduled_departure_time_range_in_minute = models.PositiveSmallIntegerField()
    owner = models.ForeignKey(User, related_name='driver_posts', on_delete=models.CASCADE)
    matching_driver = models.ForeignKey(DriverSchedule, related_name='matched_rider',on_delete=models.CASCADE)

