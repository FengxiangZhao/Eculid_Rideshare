# rest framework
from rest_framework import serializers
# local
from .models import Client
from .verifications import validate_case_email


class ClientSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Client
        fields = ('id', 'username', 'phone', 'email')

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