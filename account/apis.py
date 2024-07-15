from .models import LocationInf,BlueToothInf,AccelerometerInf,CustomUser
from .serializers import LocationSerializer,BlueToothSerializer,modifyPhoneSerializer,AccSerializer,modifyEmailSerializer,modifyPasswordSerializer,UserLoginSerializer,UserSerializer,IsPasswordSerializer,ResetSerializer,modifyNameSerializer
from .serializers import modifyGenderSerializer
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

class UpdateLocationApi(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        username = request.user.username
        serializer = LocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        device = serializer.validated_data.get('device')
        longitude = serializer.validated_data.get('longitude')
        latitude = serializer.validated_data.get('latitude')

        LocationInf.objects.create(usename=username,device=device, longitude=longitude, latitude=latitude)
                # 返回成功响应
        return Response({"message": "Data saved successfully."})

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
            return Response({'message': '请先登录'}, status=status.HTTP_400_BAD_REQUEST)

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
            return Response({'message': '请先登录'}, status=status.HTTP_400_BAD_REQUEST)


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
            return Response({'message': '请先登录'}, status=status.HTTP_400_BAD_REQUEST)

#注册api
class UserRegisterApi(APIView):
    permission_classes = []
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "用户注册成功"}, status=status.HTTP_201_CREATED)
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
            return Response({"message": "用户未注册"}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.check_password(serializer.validated_data["password"]):
            refresh: RefreshToken = RefreshToken.for_user(user)  # 生成refresh token
            return Response({
                "username": user.username,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "expire": refresh.access_token.payload["exp"] - refresh.access_token.payload["iat"],
            })
        else:
            return Response({"message": "用户登录失败，请检查您的账号密码"})
        
# 令牌发送api 通用api
class Is_PasswordApi(APIView):
    permission_classes = []
    def post(self, request: Request) -> Response:
        serializer = IsPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if get_user_model().objects.get(username=serializer.validated_data["username"]) == None:
            return Response("用户不存在")
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
                "令牌邮件已经发至您的预留邮箱，请查看！"
            })
        else:
            return Response("邮箱错误或不存在")


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
                    f"您的密码修改成功，请重新登录"
                })
            else:
                return Response({
                    "令牌超时或错误"
                })
        else :
            return Response({"用户名不存在"},status=status.HTTP_400_BAD_REQUEST)

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
                    f"您的密码修改成功，请重新登录"
                })
        return Response({"用户名不存在"},status=status.HTTP_400_BAD_REQUEST)

class modifyPhoneApi(APIView):
    permission_classes = []
    def post(self, request: Request) -> Response:
        serializer = modifyPhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        if get_user_model().objects.get(username=username):
            user = get_user_model().objects.get(username=username)
            if serializer.validated_data['token'] == user.token and timezone.now() <= user.token_expires:
                user = get_user_model().objects.get(username=serializer.validated_data['username'])
                user.phone_number = serializer.validated_data['phone_number']
                user.save()
                return Response({
                    f"您的手机号修改成功!"
                })
            else:
                return Response({
                    "令牌超时或错误"
                })
        else :
            return Response({"用户名不存在"},status=status.HTTP_404_NOT_FOUND)

class modifyEmailApi(APIView):
    permission_classes = []
    def post(self, request: Request) -> Response:
        serializer = modifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        if get_user_model().objects.get(username=username):
            user = get_user_model().objects.get(username=username)
            if serializer.validated_data['token'] == user.token and timezone.now() <= user.token_expires:
                user = get_user_model().objects.get(username=serializer.validated_data['username'])
                user.email = serializer.validated_data['email']
                user.save()
                return Response({
                    f"您的邮箱地址修改成功!"
                })
            else:
                return Response({
                    "令牌超时或错误"
                })
        else :
            return Response({"用户名不存在"},status=status.HTTP_400_BAD_REQUEST)
        
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
            return Response("性别修改成功")
        return Response({"用户名不存在"},status=status.HTTP_400_BAD_REQUEST)

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
            return Response("姓名修改成功")
        return Response({"用户名不存在"},status=status.HTTP_400_BAD_REQUEST)