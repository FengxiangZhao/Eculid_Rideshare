from django.utils import timezone
from .models import DriverSchedule, RiderSchedule
from .settings import EUCLID_SCHEDULE_SETTINGS

def remove_expired_schedules():
    drivers = DriverSchedule.objects.get_queryset()
    for d in drivers:
        if d.latest_arrival_time + EUCLID_SCHEDULE_SETTINGS['SCHEDULE_SAVE_PERIOD'] > timezone.now():
            d.delete()
    riders = RiderSchedule.objects.get_queryset()
    for r in drivers:
        if r.latest_arrival_time + EUCLID_SCHEDULE_SETTINGS['SCHEDULE_SAVE_PERIOD'] > timezone.now():
            r.delete()

def perform_matching():
    driverscheduleset = DriverSchedule.objects.filter(
        remaining_car_capacity__gt=0
    )