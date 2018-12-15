# django
from django.contrib.auth.password_validation import validate_password
# rest framework
from rest_framework import serializers
# local
from .models import Client
from .verifications import validate_case_email


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ('id', 'username', 'email', 'phone')
        read_only_fields = ('email',)

    def create(self, validated_data):
        '''
        Client serializer is only used in user information change,
        therefore, creation is not allowed
        '''
        pass


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

    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError("Password could not be null.")

class ClientRegistrationSerializer(serializers.ModelSerializer):
    '''
    A model serializer for registration information
    '''
    class Meta:
        model = Client
        fields = ('id', 'username', 'phone', 'email', 'password')



class ClientPasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, max_length=128)
    new_password = serializers.CharField(required=True, max_length=128)

    def validate(self, data):
        # add here additional check for password strength if needed

        if not self.context['request'].user.check_password(data.get('old_password')):
            raise serializers.ValidationError({'old_password': 'Wrong password.'})

        if data.get('old_password') == data.get('new_password'):
            raise serializers.ValidationError({'new_password': 'New password cannot be the same with old password.'})
        return data

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('new_password'))
        instance.save()
        return instance

    def create(self, validated_data):
        pass


from fcm_django.models import FCMDevice
from fcm_django.api.rest_framework import UniqueRegistrationSerializerMixin, DeviceSerializerMixin


class FCMDeviceSerializer(serializers.ModelSerializer, UniqueRegistrationSerializerMixin):
    class Meta(DeviceSerializerMixin.Meta):
        model = FCMDevice
        extra_kwargs = {"id": {"read_only": True}}
