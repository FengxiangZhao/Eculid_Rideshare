from django.utils import timezone
from celery import shared_task
from .models import DriverSchedule, RiderSchedule
from .settings import EUCLID_SCHEDULE_SETTINGS
from .matching import perform_matching

def remove_expired_schedules():
    drivers = DriverSchedule.objects.get_queryset()
    for d in drivers:
        if d.latest_arrival_time + EUCLID_SCHEDULE_SETTINGS['SCHEDULE_SAVE_PERIOD'] > timezone.now():
            d.delete()
    riders = RiderSchedule.objects.get_queryset()
    for r in drivers:
        if r.latest_arrival_time + EUCLID_SCHEDULE_SETTINGS['SCHEDULE_SAVE_PERIOD'] > timezone.now():
            r.delete()

@shared_task(name='perform_matching')
def perform_matching_task():
    perform_matching()

@shared_task(name='debugging')
def perform_debugging_task():
    print("Debug Test Run at", timezone.now())