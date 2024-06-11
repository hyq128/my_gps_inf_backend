from django.urls import path
from .apis import UpdateLocationApi,UpdateBTApi,UpdateACCApi,UserRegisterApi,UserLoginApi,GetUserData
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


urlpatterns = [
    path("updateAcc/", UpdateACCApi.as_view(), name="updateAcc"),
    path("updateBT/", UpdateBTApi.as_view(), name="updateBoothTooth"),
    path("updateLocation/", UpdateLocationApi.as_view(), name="updateLocation"),
    path("getdata/",GetUserData.as_view(),name="getdata"),
    path("register/", UserRegisterApi.as_view(), name="register"),
    path("login/", UserLoginApi.as_view(), name="Login"),
    path("token_obtain/", TokenObtainPairView.as_view(), name="obtain"),
    path("token_refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("token_verify/", TokenVerifyView.as_view(), name="verify"),
]
