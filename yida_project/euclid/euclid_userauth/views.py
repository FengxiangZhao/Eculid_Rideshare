# django
from django.contrib.auth import update_session_auth_hash
# rest framework
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
# local
from .permissions import IsAnonymousOrReadOnly
from .models import Client
from .serializers import ClientSerializer, ClientRegistrationSerializer, ClientPasswordChangeSerializer
from euclid_verification.models import EmailVerificationToken


class CurrentClient(generics.RetrieveUpdateAPIView):
    '''
    Retrieve, or update the current client that is logged in
    '''
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ClientSerializer

    def get_object(self):
        return self.request.user


class ClientRegistration(generics.CreateAPIView):
    permission_classes = (IsAnonymousOrReadOnly,)
    serializer_class = ClientRegistrationSerializer

    def perform_create(self, serializer):
        # Assumption that the serializer.is_valid() has been ran before perfore_create
        user = Client.objects.create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
            phone=serializer.validated_data['phone'],
        )
        token = EmailVerificationToken.objects.create_email_verification_token(user, save=False)
        token.send_verification_email()
        token.save()


class ClientPasswordChange(generics.GenericAPIView):
    """
    An endpoint for changing password.
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = ClientPasswordChangeSerializer

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.object.set_password(serializer.data.get("new_password"))
        self.object.save()
        # make sure the user stays logged in
        update_session_auth_hash(request, self.object)
        return Response(status=status.HTTP_204_NO_CONTENT)


# FCM
from fcm_django.models import FCMDevice
from .serializers import FCMDeviceSerializer

class FCMDeviceCreate(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FCMDeviceSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

        if self.request.data.get('active', True):
            FCMDevice.objects.filter(user=self.request.user).update(active=False)

