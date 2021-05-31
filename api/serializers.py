from rest_framework import serializers
from .models import DeviceManagement


class DeviceManagementSerializers(serializers.ModelSerializer):
    class Meta:
        model = DeviceManagement
        fields = "__all__"
