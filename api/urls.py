from .views import DeviceData, DeviceDataUpdate,device_data_from_device
from django.urls import path

urlpatterns = [
    path('show/<str:device_id>/', DeviceData),
    path('update/<str:device_id>/<str:relay>/<int:status>', DeviceDataUpdate),
    path('device/<str:topic>/live_data', device_data_from_device),
    # path('getid/<str:device_id>/<str:relay>/', GetDeviceId.as_view()),
]
