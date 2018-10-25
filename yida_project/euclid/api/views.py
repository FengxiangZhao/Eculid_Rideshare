# rest framework
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
# local
from .permissions import IsOwner, IsVerifiedUserOrReadOnly
from .models import DriverSchedule, RiderSchedule, Client
from .serializer import DriverScheduleSerializer, RiderScheduleSerializer, ClientSerializer, ClientRegistrationSerializer

@api_view(['GET'])
@permission_classes((permissions.AllowAny,)) # Allow any to view the API root
def api_root(request, format=None):
    '''
    provide an entry point for the API Views in the form of http links
    '''
    return Response({
        'Client Registration': reverse('client-registration', request=request, format=format),
        'Client Token Authorization' : reverse('token-auth', request=request, format=format),
        'Client Token Refresh' : reverse('token-refresh', request=request, format=format),
        'Client Information': reverse('client', request=request, format=format),
        'Driver Schedule': reverse('driver-schedule-list', request=request, format=format),
        'Rider Schedule' : reverse('rider-schedule-list', request=request, format=format)
    })


class DriverScheduleList(generics.ListCreateAPIView):
    '''
    List all driver schedules related to the user or Create new driver schedule
    '''
    permission_classes = (permissions.IsAuthenticated, IsVerifiedUserOrReadOnly, IsOwner)
    serializer_class = DriverScheduleSerializer

    def get_queryset(self):
        return DriverSchedule.objects.all().filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class DriverScheduleDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    Retrieve, update or delete a specific DriverSchedule
    '''
    permission_classes = (permissions.IsAuthenticated, IsVerifiedUserOrReadOnly, IsOwner)
    serializer_class = DriverScheduleSerializer

    def get_queryset(self):
        return DriverSchedule.objects.all().filter(owner=self.request.user)

class RiderScheduleList(generics.ListCreateAPIView):
    '''
    List all rider schedules related to the client or Create new rider schedule
    '''
    permission_classes = (permissions.IsAuthenticated, IsVerifiedUserOrReadOnly, IsOwner)
    serializer_class = RiderScheduleSerializer

    def get_queryset(self):
        return RiderSchedule.objects.all().filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class RiderScheduleDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    Retrieve, update or delete a specific RiderSchedule.
    '''
    permission_classes = (permissions.IsAuthenticated, IsVerifiedUserOrReadOnly, IsOwner)
    serializer_class = RiderScheduleSerializer

    def get_queryset(self):
        return RiderSchedule.objects.all().filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CurrentClient(generics.RetrieveUpdateAPIView):
    '''
    Retrieve, or update the current client that is logged in
    '''
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ClientSerializer

    def get_object(self):
        return self.request.user


class ClientRegistration(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ClientRegistrationSerializer

    def perform_create(self, serializer):
        # Assumption that the serializer.is_valid() has been ran before perfore_create
        user = Client.objects.create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
            phone=serializer.validated_data['phone'],
        )