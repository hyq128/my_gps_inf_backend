from .models import LocationInf,BlueToothInf,AccelerometerInf
from .serializers import LocationSerializer,BlueToothSerializer,AccSerializer
from analysis.models import gps_cluster,bt_cluster
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
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

        # 检查gps_cluster表中的现有数据
        cluster_exists = gps_cluster.objects.filter(
            Q(longitude__gte=longitude_min, longitude__lte=longitude_max) &
            Q(latitude__gte=latitude_min, latitude__lte=latitude_max) & 
            Q(username = username)
        ).exists()

        flag = 0
        if not cluster_exists:
            # 检索误差范围内、用户名匹配并且label字段为空的坐标
            nearby_locations_count = LocationInf.objects.filter(
                Q(longitude__gte=longitude_min, longitude__lte=longitude_max) &
                Q(latitude__gte=latitude_min, latitude__lte=latitude_max) &
                Q(username=username) &
                Q(label='')
            ).count()

            # 判断并设置flag
            if nearby_locations_count >= min_times:
                flag = 1
                # 保存新的聚类信息
                gps_cluster.objects.create(
                    username=username,
                    longitude=longitude,
                    latitude=latitude
                )

        # 保存新的位置信息
        LocationInf.objects.create(
            username=username,
            device=device,
            longitude=longitude,
            latitude=latitude,
            accuracy=accuracy
        )

        # 返回成功响应和flag
        return Response({
            "message": "Data saved successfully.",
            "flag": flag,
            "longitude_min": longitude_min,
            "longitude_max": longitude_max,
            "latitude_min": latitude_min,
            "latitude_max": latitude_max
        })
    
class UpdateBTApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = request.user.username
        serializer = BlueToothSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            # 这里处理数据验证错误，并返回状态码521
            return Response({"message": "Data validation error."})

        device = serializer.validated_data.get('device')
        connection_device = serializer.validated_data.get('connection_device')

        # 解析 connection_device 字段
        devices = connection_device.split(';')
        mac_counter = {}
        results = []

        # 统计 BlueToothInf 表中当前用户的 MAC 地址计数
        all_user_records = BlueToothInf.objects.filter(username=username)
        for record in all_user_records:
            conn_devices = record.connection_device.split(';')
            for conn_dev in conn_devices:
                try:
                    _, mac_addr = conn_dev.split(':', 1)
                except ValueError:
                    continue
                if mac_addr in mac_counter:
                    mac_counter[mac_addr] += 1
                else:
                    mac_counter[mac_addr] = 1

        for dev in devices:
            try:
                name, mac = dev.split(':', 1)
            except ValueError:
                continue

            # 检查是否在当前用户的 bt_cluster 中
            if bt_cluster.objects.filter(username=username, bt_device=f"{name}:{mac}").exists():
                results.append({'mac': mac, 'flag': 0})
            else:
                # 判断设备名称是否有效
                if mac_counter.get(mac, 0) > 5 and name != "undefined":
                    # 保存到 bt_cluster
                    bt_cluster.objects.create(
                        username=username,
                        bt_device=f"{name}:{mac}"
                    )
                    important=f'{name}:{mac}'
                    results.append({'important': important, 'flag': 1})
                else:
                    results.append({'mac': mac, 'flag': 0})

        # 保存到 BlueToothInf 中
        BlueToothInf.objects.create(username=username, device=device, connection_device=connection_device)

        # 返回处理结果
        return Response({"message": "Data saved successfully.", "results": results})

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


        