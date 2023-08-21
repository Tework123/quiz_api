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


class QuestionSerializer0(serializers.ModelSerializer):
    class Meta:
        model = ResultAnswer
        fields = ['id', 'user_id']


class QuestionSerializer1(serializers.ModelSerializer):
    result_answer_list = QuestionSerializer0(many=True, read_only=True)

    class Meta:
        model = Answer
        fields = ['id', 'description', 'result_answer_list']


class QuestionSerializer2(serializers.ModelSerializer):
    answer_list = QuestionSerializer1(many=True, read_only=True)

    # добавляем поле user_id
    # user_id = serializers.SerializerMethodField(method_name="get_user_id")

    # def get_user_id(self, obj):
    #     user_id = self.context['request'].user.id
    #     return user_id

    class Meta:
        model = Question
        fields = ['id', 'description', 'answer_list']


class AnswerGetSerializer(serializers.Serializer):
    answer_id = serializers.IntegerField()


# class AnswerSerializer(serializers.Serializer):
#     question_id = serializers.IntegerField()
#
#     def create(self, validated_data):
#         print(validated_data)
#         return Answer.objects.create(**validated_data)
