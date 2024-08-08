from django.db import models

class LocationInf(models.Model):
    class Meta:
        verbose_name = '定位记录'
        verbose_name_plural = '定位表'
    username = models.CharField(max_length=10, verbose_name="用户名")
    longitude = models.FloatField(default=0.0, verbose_name="经度")
    latitude = models.FloatField(default=0.0, verbose_name="纬度")
    device = models.CharField(max_length=150, default="", verbose_name="设备",blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="时间戳")
    accuracy = models.FloatField(default=0.0, verbose_name="精确范围")
    label = models.CharField(max_length=20, default="", verbose_name="用户标注")

class BlueToothInf(models.Model):
    class Meta:
        verbose_name = '蓝牙记录'
        verbose_name_plural = '蓝牙表'
    username = models.CharField(max_length=10, verbose_name="用户名")
    connection_device = models.CharField(max_length=1500000, verbose_name="连接设备")
    device = models.CharField(max_length=150, default="", verbose_name="设备",blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="时间戳")

class AccelerometerInf(models.Model):
    class Meta:
        verbose_name = '加速度计'
        verbose_name_plural = '加速度表'
    username = models.CharField(max_length=10, verbose_name="用户名")
    acc_x = models.FloatField(default=0.0, verbose_name="加速度X")
    acc_y = models.FloatField(default=0.0, verbose_name="加速度Y")
    acc_z = models.FloatField(default=0.0, verbose_name="加速度Z")
    device = models.CharField(max_length=150, default="", verbose_name="设备",null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="时间戳")

