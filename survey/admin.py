from django.contrib import admin
from django.contrib.auth.admin import *
from .models import Question,Survey,Answer


# # Register your models here.
class qusetionAdmin(admin.ModelAdmin):
    fields = ( 'question_text','question_type','choices')
    list_display = ('question_id','question_text','question_type','choices')
    list_per_page = 10
    search_fields = ['question_id']
    list_filter = ('question_id',)
    list_editable = ('question_text','question_type','choices')
admin.site.register(Question,qusetionAdmin)

class surveyAdmin(admin.ModelAdmin):
    fields = ('title','description','questions')
    list_display = ('survey_id', 'title','description','created_at','questions')
    list_per_page = 10
    search_fields = ['title']
    list_filter = ('title',)
    list_editable = ('title','description','questions')
admin.site.register(Survey,surveyAdmin)


class answerAdmin(admin.ModelAdmin):
    list_display =('response_id', 'survey_id','question_id','username','answer_text','response_date')
    list_per_page = 10
    search_fields = ['username']
    list_filter = ('survey_id',)
    list_display_links = ('survey_id',)
admin.site.register(Answer,answerAdmin)

