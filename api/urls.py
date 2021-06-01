from .views import DeviceData, DeviceDataUpdate,device_data_from_device, show_last_readings_of_device, contact_to_device
from django.urls import path

urlpatterns = [
    # path('show/<str:device_id>/', DeviceData),
    # path('update/<str:device_id>/<str:relay>/<int:status>', DeviceDataUpdate),
    path('api/post_device_data/<str:site_prefix>', device_data_from_device),
    path('api/get_live_data/<str:site_prefix>', show_last_readings_of_device),
    path('api/connect_to_device/', contact_to_device),
]
