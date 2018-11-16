#rest framework
from rest_framework import generics, permissions
# local
from .models import DriverSchedule, RiderSchedule
from .permissions import IsOwner, IsVerifiedUserOrReadOnly
from .serializers import DriverScheduleSerializer, RiderScheduleSerializer

class DriverScheduleList(generics.ListCreateAPIView):
    '''
    List all driver schedules related to the user
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
    '''
    permission_classes = (permissions.IsAuthenticated, IsVerifiedUserOrReadOnly, IsOwner)
    serializer_class = DriverScheduleSerializer

    def get_queryset(self):
        return DriverSchedule.objects.all().filter(owner=self.request.user)

    def perform_destroy(self, instance):
        '''
        User active perform cancel on a specific driver schedule
        '''
        instance._cancel()

class RiderScheduleList(generics.ListCreateAPIView):
    '''
    List all rider schedules related to the client
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

    def perform_destroy(self, instance):
        '''
        User actively perform cancel on a specific rider schedule
        '''
        instance._cancel()
