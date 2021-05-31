from django.db import models


class DeviceManagement(models.Model):
    device_id = models.CharField(max_length=10)
    relay = models.CharField(max_length=3)
    status = models.IntegerField()

    def __str__(self):
        return f"{self.device_id}, {self.relay}, {self.status}"