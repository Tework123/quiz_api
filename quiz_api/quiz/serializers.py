from django.contrib.auth.models import User
from rest_framework import serializers

from quiz.models import Quiz, Question, Answer, ResultAnswer


class QuizListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'


class QuizDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'
        lookup_field = 'slug'


class QuestionListSerializerFirst(serializers.ModelSerializer):
    class Meta:
        model = ResultAnswer
        fields = ['id', 'user_id']


class QuestionListSerializerSecond(serializers.ModelSerializer):
    result_answer_list = QuestionListSerializerFirst(many=True, read_only=True)

    class Meta:
        model = Answer
        fields = ['id', 'description', 'result_answer_list']


class QuestionListSerializerThird(serializers.ModelSerializer):
    answer_list = QuestionListSerializerSecond(many=True, read_only=True)

    # добавляем поле user_id
    # user_id = serializers.SerializerMethodField(method_name="get_user_id")

    # def get_user_id(self, obj):
    #     user_id = self.context['request'].user.id
    #     return user_id

    class Meta:
        model = Question
        fields = ['id', 'description', 'answer_list']


class QuizListStatisticsSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    questions = serializers.IntegerField()


class Quiz2(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'description']


class QuizDetailStatisticsSerializer(serializers.ModelSerializer):
    answer_list = Quiz2(many=True)

    class Meta:
        model = Question
        fields = ['id', 'description', 'answer_list']

# считаем количество пользователей, которое ответило на каждый вопрос, у каждого вопроса в сумме 100%
# надо их раскидать по ответам, так у каждого вопроса
# выводим вопрос, ответ, процент ответа, ответ, процент ответа и так далее
# может в сериализаторах это можно сделать
