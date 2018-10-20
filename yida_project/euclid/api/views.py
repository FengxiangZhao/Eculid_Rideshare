# rest framework
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
# local
from .permissions import IsOwner, IsVerifiedUserOrReadOnly
from .models import DriverSchedule, RiderSchedule, Client
from .serializer import DriverScheduleSerializer, RiderScheduleSerializer, ClientSerializer, ClientRegistrationSerializer

@api_view(['GET'])
def api_root(request, format=None):
    '''
    provide an entry point for the API Views in the form of http links
    '''
    return Response({
        'clients': reverse('client-list', request=request, format=format),
        'client registration' : reverse('client-registration', request=request, format=format),
        'driver schedule': reverse('driver-schedule-list', request=request, format=format),
        'rider schedule' : reverse('rider-schedule-list', request=request, format=format)
    })


class DriverScheduleList(generics.ListCreateAPIView):
    '''
    List all driver schedules related to the user
        'GET'  : retrieves a list of DriverSchedule
        'POST' : uploads a new DriverSchedule
    '''
    permission_classes = (permissions.IsAuthenticated, IsVerifiedUserOrReadOnly, IsOwner)
    serializer_class = DriverScheduleSerializer

    def get_queryset(self):
        return DriverSchedule.objects.all().filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class DriverScheduleDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    Retrieve, update or delete a specific DriverSchedule.
        'GET'    : retrieves the specific DriverSchedule indexed by pk
        'PUT'    : updates the specific DriverSchedule indexed by pk
        'DELETE' : deletes the specific DriverSchedule indexed by pk
    '''
    permission_classes = (permissions.IsAuthenticated, IsVerifiedUserOrReadOnly, IsOwner)
    serializer_class = DriverScheduleSerializer

    def get_queryset(self):
        return DriverSchedule.objects.all().filter(owner=self.request.user)

class RiderScheduleList(generics.ListCreateAPIView):
    '''
    List all rider schedules related to the client
        'GET'  : retrieves a list of RiderSchedule related to the client
        'POST' : uploads a new RiderSchedule
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
        'GET'    : retrieves the specific RiderSchedule indexed by pk
        'PUT'    : updates the specific RiderSchedule indexed by pk
        'DELETE' : deletes the specific RiderSchedule indexed by pk
    '''
    permission_classes = (permissions.IsAuthenticated, IsVerifiedUserOrReadOnly, IsOwner)
    serializer_class = RiderScheduleSerializer

    def get_queryset(self):
        return RiderSchedule.objects.all().filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ClientList(generics.ListAPIView):
    '''
    List client's own information
        'GET' : retrieves the client's information as a list
    '''
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ClientSerializer

    def get_queryset(self):
        '''
        Obtain the query set for the API View.
        Only returns self, if user is authenticated
        '''
        return Client.objects.all().filter(username=self.request.user.username)

class ClientDetail(generics.RetrieveUpdateAPIView):
    '''
    Retrieve, and update a specific client.
    Client could only have the permission for their own information.
        'GET' : retrieves the specific client indexed by pk
        'PUT' : updates the specific client indexed by pk
    '''
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ClientSerializer

    def get_queryset(self):
        '''
        Obtain the query set for the API View.
        Only returns self, if user is authenticated
        '''
        return Client.objects.all().filter(username=self.request.user.username)


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