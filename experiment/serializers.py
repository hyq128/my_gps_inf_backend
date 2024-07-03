from .models import expHistory
from rest_framework import serializers
from django.contrib.auth import get_user_model

class expHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model=expHistory
        field = ['start_time','end_time','exp_type']
    
    start_time = serializers.DateTimeField(
        required=True
    )

    end_time = serializers.DateTimeField(
        required=True
    )

    exp_type = serializers.CharField(
        max_length=150,
        required=True
    )