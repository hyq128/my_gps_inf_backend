from django.contrib import admin
from .models import Question, Survey, Answer

# 注册Question模型的管理员界面
class QuestionAdmin(admin.ModelAdmin):
    fields = ('question_text', 'question_type', 'choices')
    list_display = ('question_id', 'question_text', 'question_type', 'choices')
    list_per_page = 10
    search_fields = ['question_id']
    list_filter = ('question_id',)
    list_editable = ('question_text', 'question_type', 'choices')
admin.site.register(Question, QuestionAdmin)

# 注册Survey模型的管理员界面
class SurveyAdmin(admin.ModelAdmin):
    fields = ('title', 'description', 'questions')
    list_display = ('survey_id', 'title', 'description', 'created_at', 'questions','get_question_text')
    list_per_page = 10
    search_fields = ['title']
    list_filter = ('title',)
    list_editable = ('title', 'description', 'questions')
    def get_question_text(self, obj):
        res=""
        for i in obj.questions.split(';'):
            if i=='':
                continue
            res+=f"{i}."+Question.objects.get(question_id=i).question_text
        return res
    get_question_text.short_description = '具体问题'
admin.site.register(Survey, SurveyAdmin)

# 注册Answer模型的管理员界面
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('response_id', 'survey_id', 'question_id', 'get_question_text', 'answer_text', 'username', 'response_date')
    list_per_page = 10
    search_fields = ['username']
    list_filter = ('survey_id',)
    list_display_links = ('survey_id',)

    def get_question_text(self, obj):
        return Question.objects.get(question_id=obj.question_id).question_text
    get_question_text.short_description = '具体问题'

admin.site.register(Answer, AnswerAdmin)
