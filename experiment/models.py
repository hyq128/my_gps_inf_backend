from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.
class experiment(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    exp_id = models.AutoField(primary_key=True)
    exp_name = models.CharField(max_length=64)
    gps_frequency = models.IntegerField(verbose_name="GPS调用间隔(分钟)",default=-1)
    bt_frequency = models.IntegerField(verbose_name="蓝牙调用频率(分钟)",default=-1)
    acc_frequency = models.IntegerField(verbose_name="加速度调用频率(秒)",default=-1)
    participants_name = models.CharField(max_length=64,verbose_name="实验参与者",default="",blank=True)