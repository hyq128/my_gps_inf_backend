from .models import AccelerometerInf,LocationInf,BlueToothInf,CustomUser
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationInf
        fields = ['longitude', 'latitude','timestamp']

    
    longitude = serializers.FloatField(
        required=True
    )

    latitude = serializers.FloatField(
        required=True
    )

    timestamp = serializers.DateTimeField()

class BlueToothSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlueToothInf
        fields = ['connection_device','timestamp']
    
    connection_device = serializers.CharField(
        max_length=150,
        required=True
    )

    timestamp = serializers.DateTimeField()

    
class AccSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccelerometerInf
        fields = ['acc_x', 'acc_y','acc_z','timestamp']
    
    acc_x=serializers.FloatField(
        required=True
    )
    
    acc_y=serializers.FloatField(
        required=True
    )

    acc_z=serializers.FloatField(
        required=True
    )

    timestamp = serializers.DateTimeField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "username",
            "password",
            "email",
            "device"
        ]

    def create(self, validated_data: dict) -> CustomUser:
        #密码单独拿出来，因为需要加密后才能存在数据库
        password = validated_data.pop("password")
        #创建实例user
        user = get_user_model().objects.create_user(**validated_data)
        #加密
        user.set_password(password)
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):

    username = serializers.CharField(
        max_length=150,
        required=True
    )
    password = serializers.CharField(
        max_length=128,
        required=True
    )



# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         token['username'] = user.name
#         return token