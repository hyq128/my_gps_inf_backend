from django.db import models
# Create your models here.
class experiment(models.Model):
    class Meta:
        verbose_name = '实验表'
        verbose_name_plural = '实验表'
    start_time = models.DateTimeField(verbose_name="实验开始时间")
    end_time = models.DateTimeField(verbose_name="实验结束时间")
    exp_id = models.AutoField(primary_key=True ,verbose_name="实验ID")
    exp_name = models.CharField(max_length=64 ,verbose_name="实验名称",default="")
    description = models.CharField(max_length=255 ,verbose_name="实验描述",default="")
    gps_frequency = models.IntegerField(verbose_name="GPS调用间隔(分钟)",default=-1)
    bt_frequency = models.IntegerField(verbose_name="蓝牙调用频率(分钟)",default=-1)
    acc_frequency = models.IntegerField(verbose_name="加速度调用频率(秒)",default=-1)
    participants_name = models.CharField(max_length=64,verbose_name="实验参与者",default="",blank=True)
    
class exp_history(models.Model):
    class Meta:
        verbose_name = '实验历史表'
        verbose_name_plural = '实验历史表'
    username = models.CharField(max_length=10, verbose_name="用户名")
    exp_id = models.IntegerField(
        verbose_name="实验ID",
    )
    exp_name = models.CharField(
        max_length=64,
        verbose_name="实验名称",
        default="",
        blank=True,
    )