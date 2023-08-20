from django.contrib.auth.models import User
from rest_framework import serializers

from quiz.models import Quiz, Question, Answer, ResultAnswer


class QuizListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'
        lookup_field = 'slug'


# class QuestionAnswerSerializer(serializers.ModelSerializer):
#     question_id = serializers.RelatedField
#
#     class Meta:
#         model = Answer
#         fields = '__all__'

class QuestionSerializer0(serializers.ModelSerializer):
    class Meta:
        model = ResultAnswer
        fields = ['id', 'user','result']


class QuestionSerializer1(serializers.ModelSerializer):
    result_answer_list = QuestionSerializer0(many=True, read_only=True)

    class Meta:
        model = Answer
        fields = ['id', 'description', 'result_answer_list']


class QuestionSerializer2(serializers.ModelSerializer):
    answer_list = QuestionSerializer1(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'description', 'answer_list']
        # lookup_field = 'slug'


class AnswerGetSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    description = serializers.CharField()
    question_id = serializers.IntegerField()


class AnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()

    def create(self, validated_data):
        print(validated_data)
        return Answer.objects.create(**validated_data)
