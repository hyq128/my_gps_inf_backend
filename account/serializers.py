from .models import AccelerometerInf,LocationInf,BlueToothInf
from rest_framework import serializers

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