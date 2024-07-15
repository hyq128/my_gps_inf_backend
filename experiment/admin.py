from django.contrib import admin
from .models import experiment
# Register your models here.

class experimentAdmin(admin.ModelAdmin):
    fields = ( 'start_time','end_time','exp_name',"acc_frequency","bt_frequency","participants_name","gps_frequency",)
    list_display = ('exp_id','exp_name','start_time','end_time',"acc_frequency","bt_frequency","participants_name","gps_frequency",)
    list_per_page = 10
    search_fields = ['exp_name']
    list_filter = ('exp_name',)
    list_editable = ("start_time","end_time",'exp_name',"acc_frequency","bt_frequency","gps_frequency","participants_name")
admin.site.register(experiment,experimentAdmin)
