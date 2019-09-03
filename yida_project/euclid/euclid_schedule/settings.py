from django.conf import settings
from django.utils import timezone


EUCLID_SCHEDULE_SETTINGS = getattr(settings, "EUCLID_SCHEDULE_SETTINGS", {})

EUCLID_SCHEDULE_SETTINGS.setdefault("AUTH_USER_MODEL", settings.AUTH_USER_MODEL)

# The time between the trip post time and the scheduled departure time is *Lead Time*
# LEAD_CUTOFF_TIME specifies the cutoff time for matching before the departure time
# A "LEAD_CUTOFF_TIME" before the scheduled departure time, the user device will be
#   notified to obtain the trip informations
EUCLID_SCHEDULE_SETTINGS.setdefault("LEAD_CUTOFF_TIME", timezone.timedelta(minutes=20))

# Database cleaning will be performed periodically
# SCHEDULE_CLEAN_PERIOD defines how often will the database cleaning will be performed
# SCHEDULE_SAVE_PERIOD defines how long the passed schedule will be preserved
EUCLID_SCHEDULE_SETTINGS.setdefault("SCHEDULE_CLEAN_PERIOD", timezone.timedelta(days=1))
EUCLID_SCHEDULE_SETTINGS.setdefault("SCHEDULE_SAVE_PERIOD", timezone.timedelta(days=7))

#
#
EUCLID_SCHEDULE_SETTINGS.setdefault("GOOGLE_MAPS_API_KEY", None)

