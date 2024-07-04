from django.urls import path
from .apis import UpdateLocationApi,UpdateBTApi,UpdateACCApi,UserRegisterApi,UserLoginApi,GetACCData,GetBTData,GetGPSData
from .apis import modifyPasswordApi,modifyEmailApi,modifyPhoneApi,modifyGenderApi,modifyNameApi
from .apis import Is_PasswordApi,ResetPasswordApi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


urlpatterns = [
    path("updateAcc/", UpdateACCApi.as_view(), name="updateAcc"),
    path("updateBT/", UpdateBTApi.as_view(), name="updateBoothTooth"),
    path("updateLocation/", UpdateLocationApi.as_view(), name="updateLocation"),
    path("register/", UserRegisterApi.as_view(), name="register"),
    path("login/", UserLoginApi.as_view(), name="Login"),
    path("token_obtain/", TokenObtainPairView.as_view(), name="obtain"),
    path("token_refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("token_verify/", TokenVerifyView.as_view(), name="verify"),
    path("getACCdata/",GetACCData.as_view(),name="getACCdata"),
    path("getGPSdata/",GetGPSData.as_view(),name="getGPSdata"),
    path("getBTdata/",GetBTData.as_view(),name="getBTdata"),
    path("isPassword/",Is_PasswordApi.as_view(),name="isPassword"),
    path("resetPassword/",ResetPasswordApi.as_view(),name="resetPassword"),
    path("modifyPassword/",modifyPasswordApi.as_view(),name="modifyPassword"),
    path("modifyEmail/",modifyEmailApi.as_view(),name="modifyEmail"),
    path("modifyPhone/",modifyPhoneApi.as_view(),name="modifyPhone"),
    path("modifyGender/",modifyGenderApi.as_view(),name="modifyGender"),
    path("modifyName/",modifyNameApi.as_view(),name="modifyName"),
]
