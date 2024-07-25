from .models import LocationInf,BlueToothInf,AccelerometerInf,CustomUser
from .serializers import LocationSerializer,BlueToothSerializer,modifyPhoneSerializer,AccSerializer,modifyEmailSerializer,modifyPasswordSerializer,UserLoginSerializer,UserSerializer,IsPasswordSerializer,ResetSerializer,modifyNameSerializer
from .serializers import modifyGenderSerializer,userInfoSerializer,LabelSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.utils import timezone
from base import email_inf
from django.db.models import Q

class UpdateLocationApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        tolerance = 0.001
        min_times = 5
        username = request.user.username
        serializer = LocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        device = serializer.validated_data.get('device')
        longitude = serializer.validated_data.get('longitude')
        latitude = serializer.validated_data.get('latitude')
        accuracy = serializer.validated_data.get('accuracy')

        # 计算经纬度误差范围
        longitude_min = longitude - tolerance
        longitude_max = longitude + tolerance
        latitude_min = latitude - tolerance
        latitude_max = latitude + tolerance

        # 检索误差范围内、用户名匹配并且label字段为空的坐标
        nearby_locations_count = LocationInf.objects.filter(
            Q(longitude__gte=longitude_min, longitude__lte=longitude_max) &
            Q(latitude__gte=latitude_min, latitude__lte=latitude_max) &
            Q(username=username) &
            Q(label='')
        ).count()

        # 保存新的位置信息
        LocationInf.objects.create(
            username=username,
            device=device,
            longitude=longitude,
            latitude=latitude,
            accuracy=accuracy
        )

        # 判断并设置flag
        flag = 1 if nearby_locations_count >= min_times else 0

        # 返回成功响应和flag
        return Response({
            "message": "Data saved successfully.",
            "flag": flag,
            "longitude_min": longitude_min,
            "longitude_max": longitude_max,
            "latitude_min": latitude_min,
            "latitude_max": latitude_max
        })
    
class updateLabelApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        tolerance = 0.001
        username = request.user.username
        serializer = LabelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        longitude = serializer.validated_data.get('longitude')
        latitude = serializer.validated_data.get('latitude')
        label = serializer.validated_data.get('label')

        # 计算经纬度误差范围
        longitude_min = longitude - tolerance
        longitude_max = longitude + tolerance
        latitude_min = latitude - tolerance
        latitude_max = latitude + tolerance

        # 更新符合条件的记录的 label 字段
        updated_count = LocationInf.objects.filter(
            Q(username=username) &
            Q(longitude__gte=longitude_min, longitude__lte=longitude_max) &
            Q(latitude__gte=latitude_min, latitude__lte=latitude_max)
        ).update(label=label)

        # 返回成功响应和更新的记录数量
        return Response({"message": f"{updated_count} records updated successfully."}, status=status.HTTP_200_OK)
    

class UpdateBTApi(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        username = request.user.username
        serializer = BlueToothSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        device = serializer.validated_data.get('device')
        connection_device = serializer.validated_data.get('connection_device')

        BlueToothInf.objects.create(username=username, device=device, connection_device =connection_device)
                # 返回成功响应
        return Response({"message": "Data saved successfully."})


class UpdateACCApi(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        username = request.user.username
        serializer = AccSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        device = serializer.validated_data.get('device')
        acc_x = serializer.validated_data.get('acc_x')
        acc_y = serializer.validated_data.get('acc_y')
        acc_z = serializer.validated_data.get('acc_z')

        AccelerometerInf.objects.create(username=username,device=device, acc_y=acc_y,acc_x=acc_x,acc_z=acc_z)
                # 返回成功响应
        return Response({"message": "Data saved successfully."})



class GetACCData(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        username = request.user.username
        if username:
            # 获取与设备相关的加速计信息
            accs = AccelerometerInf.objects.filter(username=username)
            acc_serializer = AccSerializer(accs, many=True)
            # 返回数据
            return Response({
                'username':username,
                'accelerometers': acc_serializer.data,
            })
        else:
            return Response({'message': 'Please log in first'}, status=status.HTTP_400_BAD_REQUEST)

class GetGPSData(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        username = request.user.username
        if username:
            # 获取与设备相关的位置信息
            locations = LocationInf.objects.filter(username=username)
            location_serializer = LocationSerializer(locations, many=True)
            # 返回数据
            return Response({
                'username':username,
                'Locations':location_serializer.data,
            })
        else:
            return Response({'message': 'Please log in first'}, status=status.HTTP_400_BAD_REQUEST)


class GetBTData(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        username = request.user.username
        if username:
            # 获取与设备相关的蓝牙信息
            bluetooths = BlueToothInf.objects.filter(username=username)
            bluetooth_serializer = BlueToothSerializer(bluetooths, many=True)
            # 返回数据
            return Response({
                'username':username,
                'bluetooths': bluetooth_serializer.data,
            })
        else:
            return Response({'message': 'Please log in first'}, status=status.HTTP_400_BAD_REQUEST)

class getUserInfoApi(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        username = request.user.username
        user = get_object_or_404(CustomUser, username=username)
        seri=userInfoSerializer(user)
        return Response(seri.data)
        
    
#注册api
class UserRegisterApi(APIView):
    permission_classes = []
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registration succeeded"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UserLoginApi(APIView):
    permission_classes = []
    def post(self, request: Request) -> Response:
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = get_user_model().objects.get(username=serializer.validated_data["username"])
        except ObjectDoesNotExist:
            return Response({"message": "User not registered"}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.check_password(serializer.validated_data["password"]):
            refresh: RefreshToken = RefreshToken.for_user(user)  # 生成refresh token
            return Response({
                "username": user.username,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "expire": refresh.access_token.payload["exp"] - refresh.access_token.payload["iat"],
            })
        else:
            return Response({"message": "User login failed, please check your account password"})
        
# 令牌发送api 通用api
class Is_PasswordApi(APIView):
    permission_classes = []
    def post(self, request: Request) -> Response:
        serializer = IsPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if get_user_model().objects.get(username=serializer.validated_data["username"]) == None:
            return Response("用户不存在",status=status.HTTP_400_BAD_REQUEST)
        user = get_user_model().objects.get(username=serializer.validated_data["username"])
        if user.email == serializer.validated_data["email"]:
            token_value = get_random_string(length=6)
            user.token = token_value
            user.token_expires = timezone.now() + timezone.timedelta(minutes=2)  # 设置2分钟后过期
            user.save()
            send_mail(
                '重置密码',
                message=f'您正在尝试找回密码或者修改其他验证信息，您的令牌是{token_value}',
                from_email=email_inf.EMAIL_FROM,
                recipient_list=[user.email],
            )
            return Response({
                "Token email has been sent to your reserved mailbox, please check!"
            })
        else:
            return Response("The mailbox is incorrect or does not exist",status=status.HTTP_400_BAD_REQUEST)


# 后续感觉需要添加验证码等防爆破
class ResetPasswordApi(APIView):
    permission_classes = []
    def post(self, request: Request) -> Response:
        serializer = ResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        if get_user_model().objects.get(username=username):
            user = get_user_model().objects.get(username=username)
            if serializer.validated_data['token'] == user.token and user.token_expires and timezone.now() <= user.token_expires:
                user = get_user_model().objects.get(username=serializer.validated_data['username'])
                # 更新密码前，先使用 set_password 方法加密密码
                user.set_password(serializer.validated_data['password'])
                user.save()
                return Response({
                    f"Your password has been changed successfully. Please log in again"
                })
            else:
                return Response({
                    "令牌超时或错误"
                })
        else :
            return Response({"The user name does not exist"},status=status.HTTP_400_BAD_REQUEST)

class modifyPasswordApi(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request:Request) -> Response:
        serializer = modifyPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.user.username
        if get_user_model().objects.get(username=username):
            user = get_user_model().objects.get(username=username)
            if user.check_password(serializer.validated_data['old_password']):
                user.set_password(serializer.validated_data['password'])
                user.save()
                return Response({
                    f"Your password has been changed successfully. Please log in again"
                })
        return Response({"The user name does not exist"},status=status.HTTP_400_BAD_REQUEST)

# class modifyPhoneApi(APIView):
#     permission_classes = []
#     def post(self, request: Request) -> Response:
#         serializer = modifyPhoneSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         username = serializer.validated_data['username']
#         if get_user_model().objects.get(username=username):
#             user = get_user_model().objects.get(username=username)
#             if serializer.validated_data['token'] == user.token and timezone.now() <= user.token_expires:
#                 user = get_user_model().objects.get(username=serializer.validated_data['username'])
#                 user.phone_number = serializer.validated_data['phone_number']
#                 user.save()
#                 return Response({
#                     f"您的手机号修改成功!"
#                 })
#             else:
#                 return Response({
#                     "令牌超时或错误"
#                 })
#         else :
#             return Response({"The user name does not exist"},status=status.HTTP_404_NOT_FOUND)

# class modifyEmailApi(APIView):
#     permission_classes = []
#     def post(self, request: Request) -> Response:
#         serializer = modifyEmailSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         username = serializer.validated_data['username']
#         if get_user_model().objects.get(username=username):
#             user = get_user_model().objects.get(username=username)
#             if serializer.validated_data['token'] == user.token and timezone.now() <= user.token_expires:
#                 user = get_user_model().objects.get(username=serializer.validated_data['username'])
#                 user.email = serializer.validated_data['email']
#                 user.save()
#                 return Response({
#                     f"Your email address has been successfully modified!"
#                 })
#             else:
#                 return Response({
#                     "令牌超时或错误"
#                 })
#         else :
#             return Response({"The user name does not exist"},status=status.HTTP_400_BAD_REQUEST)

# 无安全验证版本
class modifyEmailApi(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request:Request) -> Response:
        serializer = modifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.user.username
        if get_user_model().objects.get(username=username):
            user = get_user_model().objects.get(username=username)
            user.email= serializer.validated_data['email']
            user.save()
            return Response("email modification successful")
        return Response({"The user name does not exist"},status=status.HTTP_400_BAD_REQUEST)

class modifyPhoneApi(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request:Request) -> Response:
        serializer = modifyPhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.user.username
        if get_user_model().objects.get(username=username):
            user = get_user_model().objects.get(username=username)
            user.phone_number= serializer.validated_data['phone_number']
            user.save()
            return Response("phone modification successful")
        return Response({"The user name does not exist"},status=status.HTTP_400_BAD_REQUEST)

        
class modifyGenderApi(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request:Request) -> Response:
        serializer = modifyGenderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.user.username
        if get_user_model().objects.get(username=username):
            user = get_user_model().objects.get(username=username)
            user.gender= serializer.validated_data['gender']
            user.save()
            return Response("Gender modification successful")
        return Response({"The user name does not exist"},status=status.HTTP_400_BAD_REQUEST)

class modifyNameApi(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request:Request) -> Response:
        serializer = modifyNameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.user.username
        if get_user_model().objects.get(username=username):
            user = get_user_model().objects.get(username=username)
            user.name= serializer.validated_data['name']
            user.save()
            return Response("Name changed successfully")
        return Response({"The user name does not exist"},status=status.HTTP_400_BAD_REQUEST)