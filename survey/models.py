from django.db import models

class Survey(models.Model):
    class Meta:
        verbose_name = '调查问卷'
        verbose_name_plural = '调查问卷表'
    survey_id = models.AutoField(primary_key=True,verbose_name="问卷ID")
    title = models.CharField(max_length=200,verbose_name="问卷标题")
    description = models.TextField(verbose_name="问卷描述",blank=True)
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    questions= models.CharField(max_length=200,verbose_name="问卷包含的问题ID")

class Question(models.Model):
    class Meta:
        verbose_name = '问题'
        verbose_name_plural = '问题表'
    question_id = models.AutoField(primary_key=True,verbose_name="问题ID")
    question_text = models.CharField(max_length=200,verbose_name="问题文本")
    question_type = models.CharField(max_length=20, choices=[('text', 'Text'), ('choice', 'Choice'), ('rating', 'Rating')],verbose_name="问题类型")
    choices = models.TextField(null=True, blank=True,verbose_name="选择项")

class Answer(models.Model):
    class Meta:
        verbose_name = '问卷回答'
        verbose_name_plural = '问卷回答表'
    response_id = models.AutoField(primary_key=True,verbose_name="响应ID")
    survey_id = models.IntegerField(verbose_name="问卷ID")
    question_id = models.IntegerField(verbose_name="问题ID")
    username = models.CharField(max_length=20,verbose_name="回答者用户名")
    answer_text = models.TextField(verbose_name="回答文本")
    response_date = models.DateTimeField(auto_now_add=True,verbose_name="响应日期")
