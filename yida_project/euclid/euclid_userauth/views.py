# rest framework
from rest_framework import generics, permissions
# local
from .permissions import IsAnonymousOrReadOnly
from .models import Client
from .serializers import ClientSerializer, ClientRegistrationSerializer
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