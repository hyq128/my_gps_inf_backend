from django.db import models
from django.contrib.auth.models import AbstractUser

class LocationInf(models.Model):
    longitude = models.FloatField(default=0.0)
    latitude = models.FloatField(default=0.0)
    device = models.CharField(max_length=150, default="")
    timestamp = models.DateTimeField(auto_now_add=True)  # 添加记录时间的字段

class BlueToothInf(models.Model):
    connection_device = models.CharField(max_length=150, default="")
    device = models.CharField(max_length=150, default="")
    timestamp = models.DateTimeField(auto_now_add=True)  # 添加记录时间的字段

class AccelerometerInf(models.Model):
    acc_x = models.FloatField(default=0.0)
    acc_y = models.FloatField(default=0.0)
    acc_z = models.FloatField(default=0.0)
    device = models.CharField(max_length=150, default="")
    timestamp = models.DateTimeField(auto_now_add=True)  # 添加记录时间的字段
    
class CustomUser(AbstractUser):
    device = models.CharField(max_length=150, default="")
