from .models import DeviceManagement
from .serializers import DeviceManagementSerializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import HttpResponse


@api_view(["GET"])
def DeviceData(request, **kwargs):
    try:
        details = DeviceManagement.objects.filter(device_id=kwargs['device_id'])
        serializer = DeviceManagementSerializers(details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def DeviceDataUpdate(request, **kwargs):
    try:
        details = DeviceManagement.objects.filter(device_id=kwargs['device_id'], relay=kwargs['relay'])
        details.status = int(kwargs['status'])
        for i in details:
            i.status = kwargs['status']
            i.save()
        serializer = DeviceManagementSerializers(details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def device_data_from_device(request,**kwarsg):
    data = request.data
    return Response(data)
