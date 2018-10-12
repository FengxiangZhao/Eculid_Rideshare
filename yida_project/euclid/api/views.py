from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework import generics

from .models import DriverSchedule, RiderSchedule, Client
from .serializer import DriverScheduleSerializer, RiderScheduleSerializer, ClientSerializer

# handles the driverschedule

@api_view(['GET', 'POST'])
def driverSchedule_list(request):
    """
    List all driver schedules
    request: User's request to the server
        'GET'  : returns a list of driverschdule
        'POST' : uploades a new driverschedule
    """
    if request.method == 'GET':
        schedule = DriverSchedule.objects.all()
        serializer = DriverScheduleSerializer(schedule, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DriverScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def driverschedule_detail(request, pk):
    """
    Retrieve, update or delete a specific driverschedule.
    request : User's request
    pk      : The primary key index of the specific driverschedule in the database
                If the pk does not exist, return 404-NOT-FOUND

        'GET'    : returns the specific driverschedule indexed by pk
        'PUT'    : updates the specific driverschedule indexed by pk
        'DELETE' : deletes the specific driverschedule indexed by pk
    """
    try:
        schedule = DriverSchedule.objects.get(pk=pk)
    except DriverSchedule.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DriverScheduleSerializer(schedule)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DriverScheduleSerializer(schedule, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        schedule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Rider schedule handler


@api_view(['GET', 'POST'])
def riderschedule_list(request):
    """
    List all riderschedules
    request: User's request to the server
        'GET'  : returns a list of riderschedule
        'POST' : uploads a new riderschedule
    """
    if request.method == 'GET':
        schedule = RiderSchedule.objects.all()
        serializer = RiderScheduleSerializer(schedule, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RiderScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def riderschedule_detail(request, pk):
    """
    Retrieve, update or delete a specific riderschedule.
    request : User's request
    pk      : The primary key index of the specific riderschedule in the database
                If the pk does not exist, return 404-NOT-FOUND

        'GET'    : returns the specific riderschedule indexed by pk
        'PUT'    : updates the specific riderschedule indexed by pk
        'DELETE' : deletes the specific riderschedule indexed by pk
    """
    try:
        schedule = RiderSchedule.objects.get(pk=pk)
    except RiderSchedule.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RiderScheduleSerializer(schedule)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RiderScheduleSerializer(schedule, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        schedule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ClientList(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer