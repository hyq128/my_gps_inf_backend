from .models import experiment
from rest_framework import serializers

class seeExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model=experiment
        fields = ['exp_name','start_time','end_time','gps_frequency','acc_frequency','bt_frequency']