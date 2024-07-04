from .models import AccelerometerInf,LocationInf,BlueToothInf,CustomUser
from rest_framework import serializers
from django.contrib.auth import get_user_model

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationInf
        fields = ['longitude', 'latitude','timestamp','device']

    longitude = serializers.FloatField(
        required=True
    )

    latitude = serializers.FloatField(
        required=True
    )

    timestamp = serializers.DateTimeField(
        required=False
    )
    device = serializers.CharField(
        max_length=150,
        required=True
    )

class BlueToothSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlueToothInf
        fields = ['connection_device','device','timestamp']
    
    connection_device = serializers.CharField(
        max_length=1500000,
        required=True
    )

    device = serializers.CharField(
        max_length=150,
        required=True
    )
    timestamp = serializers.DateTimeField(
        required=False
    )

    
class AccSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccelerometerInf
        fields = ['acc_x', 'acc_y','acc_z','timestamp','device']
    
    acc_x=serializers.FloatField(
        required=True
    )
    
    acc_y=serializers.FloatField(
        required=True
    )

    acc_z=serializers.FloatField(
        required=True
    )

    timestamp = serializers.DateTimeField(
        required=False
    )    
    device = serializers.CharField(
        max_length=150,
        required=True
    )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "username",
            "password",
            "email",
            "device",
            "phone_number",
            "name",
        ]
    email = serializers.EmailField(
        required=True
    )
    name = serializers.CharField(
        max_length=20,
        required=True
    )

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

# 通用验阵
class IsPasswordSerializer(serializers.Serializer):
    email=serializers.CharField(
       required=True
    )
    username = serializers.CharField(
        max_length=150,
        required=True
    )

class ResetSerializer(serializers.Serializer):
    token=serializers.CharField(
        required=True
    )
    username = serializers.CharField(
        max_length=150,
        required=True
    )
    password= serializers.CharField(
        max_length=128,
        required=True
    )

class modifyPasswordSerializer(serializers.Serializer):
    password= serializers.CharField(
        max_length=128,
        required=True
    )

    old_password= serializers.CharField(
        max_length=128,
        required=True
    )


# 手机号修改
class modifyPhoneSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        required=True
    )
    
    phone_number= serializers.CharField(
        max_length=11,
        required=True
    )
    token=serializers.CharField(
        required=True
    )

# 邮箱修改
class modifyEmailSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        required=True
    )
    email= serializers.CharField(
        max_length=150,
        required=True
    )
    token=serializers.CharField(
        required=True
    )

class modifyGenderSerializer(serializers.Serializer):
    gender= serializers.CharField(
        max_length=10,
        required=True
    )

class modifyNameSerializer(serializers.Serializer):
    name= serializers.CharField(
        max_length=20,
        required=True
    )

# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         token['username'] = user.name
#         return token