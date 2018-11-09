# django
from django.conf import settings
# rest framwork
from rest_framework import serializers
# local
from .models import DriverSchedule, RiderSchedule
from euclid_authorization.serializers import ClientSerializer

class RiderScheduleSerializer(serializers.ModelSerializer):

    owner = ClientSerializer(required=False, read_only=True)
    matching_driver = ClientSerializer(required=False, read_only=True)

    class Meta:
        model = RiderSchedule
        fields = ('id',
                  'origin_lon', 'origin_lat', 'destination_lon', 'destination_lat',
                  'scheduled_departure_datetime',
                  'scheduled_departure_time_range_in_minute',
                  'matching_driver', 'owner')

        read_only_fields = ('matching_driver',)
        depth = 2

class DriverScheduleSerializer(serializers.ModelSerializer):

    owner = ClientSerializer(required=False, read_only=True)
    matched_rider = ClientSerializer(many=True, required=False, read_only=True)


    class Meta:
        model = DriverSchedule
        fields = ('id',
                  'origin_lon', 'origin_lat', 'destination_lon', 'destination_lat',
                  'car_capacity',
                  'scheduled_departure_datetime',
                  'scheduled_departure_time_range_in_minute',
                  'driver_time_constraint_in_minute',
                  'owner', 'matched_rider',)
        depth = 2

