from .models import DeviceManagement
from .serializers import DeviceManagementSerializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import HttpResponse
import json, os, datetime
import paho.mqtt.publish as publish
import time, os

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
            json.dump(data, f)
        return Response(data, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def show_last_readings_of_device(request, **kwargs):
    try:
        site_prefix = kwargs.get("site_prefix")
        message = {"cmd": "Do something"}
        message = json.dumps(message).encode("utf-8")
        publish.single(site_prefix, message, hostname="test.mosquitto.org")
        time.sleep(2)
        with open("temp_database//"+site_prefix+".json", "r") as f:
            data = json.loads(f.read())
            print(datetime.datetime.now())
            time_stamp = data.get("time_stamp")
            dt_object = datetime.datetime.strptime(time_stamp, "%Y-%m-%d %H:%M:%S.%f")
            compare = datetime.datetime.now() - dt_object
            days, seconds = compare.days, compare.seconds
            hours = days * 24 + seconds // 3600
            # minutes = (seconds % 3600) // 60
            # seconds = seconds % 60
            if hours >= 1 and hours <= 2:
                data["device_status"] = "Delay"
            elif hours >= 3:
                data["device_status"] = "Offline"
            else:
                data["device_status"] = "Online"
            # os.remove("temp_database//"+site_prefix+".json")
            return HttpResponse(json.dumps(data), status=status.HTTP_200_OK, content_type='application/json')
    except:
        return HttpResponse('{"Message": "Device Details Not found."}', content_type='application/json')


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
