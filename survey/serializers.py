from rest_framework import serializers
from .models import Survey, Question, Answer

class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ['survey_id', 'title', 'description', 'created_at', 'questions']
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()
    questions = serializers.CharField()

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['question_id', 'question_text', 'question_type', 'choices']
    question_text = serializers.CharField(max_length=200)
    question_type = serializers.CharField(max_length=20)
    

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['response_id', 'survey_id', 'question_id', 'username', 'answer_text', 'response_date']
