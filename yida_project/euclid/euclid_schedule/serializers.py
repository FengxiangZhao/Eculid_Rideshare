# django
from django.conf import settings
# rest framwork
from rest_framework import serializers
# local
from .models import DriverSchedule, RiderSchedule
from euclid_userauth.serializers import ClientSerializer


class BaseScheduleSerializer(serializers.ModelSerializer):
    owner = ClientSerializer(required=False, read_only=True)

    class Meta:
        fields = '__all__'


class DriverScheduleSerializer(serializers.ModelSerializer):
    class Meta(BaseScheduleSerializer.Meta):
        model = DriverSchedule
        read_only_fields = ("remaining_car_capacity",)

    def create(self, validated_data):
        validated_data["remaining_car_capacity"] = validated_data["car_capacity"]
        return super(DriverScheduleSerializer, self).create(validated_data)


class RiderScheduleSerializer(serializers.ModelSerializer):
    matching_driver = DriverScheduleSerializer(required=False, read_only=True)

    class Meta(BaseScheduleSerializer.Meta):
        model = RiderSchedule
        read_only_fields = ('matching_driver',)

    def create(self, validated_data):
        validated_data["remaining_car_capacity"] = validated_data["car_capacity"]
        return super(RiderScheduleSerializer, self).create(validated_data)

