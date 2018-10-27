# rest framework
from rest_framework import generics, permissions
# local
from .permissions import IsOwner, IsVerifiedUserOrReadOnly
from .models import DriverSchedule, RiderSchedule
from .serializers import DriverScheduleSerializer, RiderScheduleSerializer

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
