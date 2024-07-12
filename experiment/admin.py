from django.contrib import admin
from .models import experiment,expHistory
# Register your models here.

# class experimentAdmin(admin.ModelAdmin):
#     fields = ( 'question_text','question_type','choices')
#     list_display = ('question_id','question_text','question_type','choices')
#     list_per_page = 10
#     search_fields = ['question_id']
#     list_filter = ('question_id',)
#     list_editable = ('question_text','question_type','choices')
# admin.site.register(Question,qusetionAdmin)
