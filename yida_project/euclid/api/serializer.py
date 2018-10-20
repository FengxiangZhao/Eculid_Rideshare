# rest framework
from rest_framework import serializers
# local
from .models import DriverSchedule, RiderSchedule, Client
from .verifications import validate_case_email


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    driver_posts = serializers.PrimaryKeyRelatedField(many=True, queryset=DriverSchedule.objects.all())
    rider_posts = serializers.PrimaryKeyRelatedField(many=True, queryset=RiderSchedule.objects.all())

    class Meta:
        model = Client
        fields = ('id', 'username', 'phone', 'email', 'driver_posts', 'rider_posts')

    def validate_email(self, value):
        '''
        Args:
            value: the value to be validated regarding email field
        Returns: the validated value
        Raises:
            serializers.ValidationError: if the value is not an email address, or is not a valid email address
        '''

        if not validate_case_email(value):
            raise serializers.ValidationError("The email address provided is not a valid CWRU email address.")
        return value

class ClientRegistrationSerializer(serializers.ModelSerializer):
    '''
    A model serializer for registration information
    '''
    class Meta:
        model = Client
        fields = ('id', 'username', 'phone', 'email', 'password')

class DriverScheduleSerializer(serializers.ModelSerializer):
    '''
    A model serializer that serializes the DriverSchedule model
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


class RiderScheduleSerializer(serializers.ModelSerializer):
    '''
    A model serializer that serializes the RiderSchedule model
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
