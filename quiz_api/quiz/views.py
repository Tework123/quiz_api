from django.contrib.auth.models import User
from django.contrib.postgres.aggregates import StringAgg
from django.db.models import CharField
from django.db.models.functions import Cast
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from quiz.models import Quiz, Question, Answer
from quiz.serializers import QuizListSerializer, QuizSerializer, AnswerSerializer, \
    AnswerGetSerializer, QuestionSerializer2


class QuizApiViewList(generics.ListAPIView):
    serializer_class = QuizListSerializer

    def get_queryset(self):
        print(self.request.user)
        return Quiz.objects.all()


# взять один quiz
class QuizApiView(generics.RetrieveAPIView):
    serializer_class = QuizSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        slug = self.kwargs.get(self.lookup_field)
        return Quiz.objects.filter(slug=slug)

    # def get_object(self, queryset=None):
    #     print(self.kwargs['pk'])
    #     return Quiz.objects.filter(id=self.kwargs['pk'])

    # queryset = Quiz.objects.all()


class QuestionApiViewList(generics.ListAPIView):
    serializer_class = QuestionSerializer2
    lookup_field = 'slug'

    def get_queryset(self):
        slug = self.kwargs.get(self.lookup_field)
        user = self.request.user
        # как будто надо достать сначала все пустые вопросы, вообще без таблицы ответов,
        # а потом все заполненные для этого пользователя, и если есть ответы, то вставить их на фронте

        data = Question.objects.filter(quiz__slug=slug, answer_list__result_answer_list__id=user.id)
        return data


#     можно посмотреть, что делает ModelViewSet, он вроде гибкий
#     в любом случае надо разные посмотреть и выбрать адекватные

# class AnswerApiView(generics.CreateAPIView, generics.RetrieveUpdateDestroyAPIView):
class AnswerApiView(APIView):
    def get(self, request, *args, **kwargs):
        print(kwargs['pk'])
        pk = kwargs['pk']
        answer = Answer.objects.filter(pk=pk)
        print(answer)
        serializer = AnswerGetSerializer(answer, many=True)

        return Response({'new_answer': serializer.data})

    def post(self, request, *args, **kwargs):
        print(request.data['id'])
        id = request.data['id']

        answer = Answer.objects.create(question_id=id)
        return Response({'new_answer': AnswerSerializer(answer).data})

# class AnswerApiView(generics.CreateAPIView, generics.RetrieveUpdateDestroyAPIView):
#     serializer_class =
#     queryset = Quiz.objects.all()


# class QuizApiViewList(APIView):
#     def get(self, request):
#         print(self.request.user)
#
#         quiz = Quiz.objects.all()
#         return Response({'quiz': quiz})


# data = Question.objects.annotate(
# answers=StringAgg(Cast('answer__description',
#                        output_field=CharField()),
#                   delimiter=', ')).filter(quiz__slug=slug)

# SELECT * FROM quiz_quiz
# FULL OUTER JOIN quiz_question USING("id")
# FULL OUTER JOIN quiz_answer USING("id")
# FULL OUTER JOIN quiz_resultanswer USING("id")
# FULL OUTER JOIN quiz_resultanswer_user USING("id")
# WHERE quiz_quiz.slug = 'dota2' OR (quiz_quiz.slug = 'dota2' AND quiz_resultanswer_user.user_id=1);
