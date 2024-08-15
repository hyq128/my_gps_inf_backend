from django.urls import path
from .apis import UpdateLocationApi,UpdateBTApi,UpdateACCApi,GetACCData,GetBTData,GetGPSData,GetGyroData,UpdateGyroApi
from .apis import GetBatteryData,updateBatteryApi


urlpatterns = [
    path("updateAcc/", UpdateACCApi.as_view(), name="updateAcc"),
    path("updateBT/", UpdateBTApi.as_view(), name="updateBoothTooth"),
    path("updateLocation/", UpdateLocationApi.as_view(), name="updateLocation"),
    path("getACCdata/",GetACCData.as_view(),name="getACCdata"),
    path("getGPSdata/",GetGPSData.as_view(),name="getGPSdata"),
    path("getBTdata/",GetBTData.as_view(),name="getBTdata"),
    path("getGyrodata/",GetGyroData.as_view(),name="getGyrodata"),
    path("updateGyro/",UpdateGyroApi.as_view(),name="updateGyro"),
    path("getBatterydata/",GetBatteryData.as_view(),name="getBatteryData"),
    path("updateBattery/",updateBatteryApi.as_view(),name="updateBattery"),
]
