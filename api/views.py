from .models import DeviceManagement
from .serializers import DeviceManagementSerializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import HttpResponse
import json, os
import paho.mqtt.publish as publish


try: os.mkdir("temp_database")
except:pass


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
def device_data_from_device(request,**kwargs):
    try:
        data = request.data
        site_prefix = kwargs.get("site_prefix")

        with open("temp_database//"+site_prefix+".json", "w") as f:
            f.write(str(data))
        return Response(data, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(["GET"])
def show_last_readings_of_device(request, **kwargs):
    try:
        site_prefix = kwargs.get("site_prefix")
        with open("temp_database//"+site_prefix+".json", "r") as f:
            data = f.read()
        return HttpResponse(data, status=status.HTTP_200_OK, content_type='application/json')
    except:
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def contact_to_device(request,**kwargs):
    try:
        data = request.data
        data1 = data.get("device_details")
        prefix = data1.get("prefix")
        message = json.dumps(data).encode("utf-8")
        if prefix != "N/A":
            publish.single(prefix, message, hostname="test.mosquitto.org", retain=True)
        return Response(data)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
