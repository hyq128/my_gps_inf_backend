from .models import LocationInf,BlueToothInf,AccelerometerInf
from .serializers import LocationSerializer,BlueToothSerializer,AccSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

class UpdateLocationApi(APIView):
    def post(self,request):
        serializer = LocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        device = serializer.validated_data.get('device')
        longitude = serializer.validated_data.get('longitude')
        latitude = serializer.validated_data.get('latitude')

        LocationInf.objects.create(device=device, longitude=longitude, latitude=latitude)
                # 返回成功响应
        return Response({"message": "Data saved successfully."})

class UpdateBTApi(APIView):
    def post(self,request):
        serializer = BlueToothSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        device = serializer.validated_data.get('device')
        connection_device = serializer.validated_data.get('connection_device')

        BlueToothInf.objects.create(device=device, connection_device =connection_device)
                # 返回成功响应
        return Response({"message": "Data saved successfully."})


class UpdateACCApi(APIView):
    def post(self,request):
        serializer = AccSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        device = serializer.validated_data.get('device')
        acc_x = serializer.validated_data.get('acc_x')
        acc_y = serializer.validated_data.get('acc_y')
        acc_z = serializer.validated_data.get('acc_z')

        AccelerometerInf.objects.create(device=device, acc_y=acc_y,acc_x=acc_x,acc_z=acc_z)
                # 返回成功响应
        return Response({"message": "Data saved successfully."})
