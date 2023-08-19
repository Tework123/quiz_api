from django.contrib.auth.models import User
from rest_framework import serializers

from quiz.models import Quiz, Question, Answer


class QuizListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class AnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()

    def create(self, validated_data):
        return Answer.objects.create(**validated_data)
