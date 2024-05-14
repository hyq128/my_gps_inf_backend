from .models import AccelerometerInf,LocationInf,BlueToothInf,CustomUser
from rest_framework import serializers
from django.contrib.auth import get_user_model

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationInf
        fields = ['device', 'longitude', 'latitude']

    device = serializers.CharField(
        max_length=150,
        required=True
    )
    
    longitude = serializers.FloatField(
        required=True
    )

    latitude = serializers.FloatField(
        required=True
    )


class BlueToothSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlueToothInf
        fields = ['device', 'connection_device']

    device = serializers.CharField(
        max_length=150,
        required=True
    )
    
    connection_device = serializers.CharField(
        max_length=150,
        required=True
    )

    
class AccSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccelerometerInf
        fields = ['device', 'acc_x', 'acc_y','acc_z']

    device = serializers.CharField(
        max_length=150,
        required=True
    )
    
    acc_x=serializers.FloatField(
        required=True
    )
    
    acc_y=serializers.FloatField(
        required=True
    )

    acc_z=serializers.FloatField(
        required=True
    )


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

