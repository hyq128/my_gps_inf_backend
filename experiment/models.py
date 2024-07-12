from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.
class expHistory(models.Model):
    username = models.CharField(max_length=10)
    start_time = models.DateTimeField()
    end_time = models.DateField()
    state = models.CharField(max_length=64)
    exp_type = models.CharField(max_length=64)

class experiment(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateField()
    exp_id = models.AutoField(primary_key=True)
    exp_name = models.CharField(max_length=64)