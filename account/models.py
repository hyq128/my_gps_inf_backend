from django.db import models


class LocationInf(models.Model):
    longitude = models.FloatField(
        default=0.0
    )
    latitude = models.FloatField(
        default=0.0
    )
    device = models.CharField(
        max_length=150,
        default=""
    )


class BlueToothInf(models.Model):

    connection_device= models.CharField(
        max_length=150,
        default=""
    )
    device = models.CharField(
        max_length=150,
        default=""
    )


class AccelerometerInf(models.Model):
    acc_x = models.FloatField(default=0.0)
    acc_y = models.FloatField(default=0.0)
    acc_z = models.FloatField(default=0.0)
    device = models.CharField(
        max_length=150,
        default=""
    )
