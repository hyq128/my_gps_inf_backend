from django.db import models

class Survey(models.Model):
    survey_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    questions= models.CharField(max_length=200)

class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    question_text = models.CharField(max_length=200)
    question_type = models.CharField(max_length=20, choices=[('text', 'Text'), ('choice', 'Choice'), ('rating', 'Rating')])
    choices = models.TextField(null=True, blank=True)

class Answer(models.Model):
    response_id = models.AutoField(primary_key=True)
    survey_id = models.IntegerField()
    question_id = models.IntegerField()
    username = models.CharField(max_length=20)
    answer_text = models.TextField()
    response_date = models.DateTimeField(auto_now_add=True)
