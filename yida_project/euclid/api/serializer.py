from rest_framework.serializers import ModelSerializer
from .models import DriverSchedule, RiderSchedule


class DriverScheduleSerializer(ModelSerializer):
    ''' A model serializer that serializes the DriverSchedule model
    '''
    class Meta:
        model = DriverSchedule
        fields = ('id',
                  'origin_lon', 'origin_lat', 'destination_lon', 'destination_lat',
                  'created_time', 'modified_time',
                  'scheduled_departure_datetime',
                  'scheduled_departure_time_range_in_minute',
                  'driver_time_constraint_in_minute',
                  'owner'
                  )

class RiderScheduleSerializer(ModelSerializer):
    ''' A model serializer that serializes the RiderSchedule model
    '''
    class Meta:
        model = RiderSchedule
        fields = ('id',
                  'origin_lon', 'origin_lat', 'destination_lon', 'destination_lat',
                  'created_time', 'modified_time',
                  'scheduled_departure_datetime',
                  'scheduled_departure_time_range_in_minute',
                  'owner', 'matching_driver'
                  )