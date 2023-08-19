from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from quiz.models import Quiz, Question, Answer
from quiz.serializers import QuizListSerializer, QuizSerializer, QuestionSerializer, AnswerSerializer


class QuizApiViewList(generics.ListAPIView):
    serializer_class = QuizListSerializer

    def get_queryset(self):
        print(self.request.user)
        return Quiz.objects.all()


# взять один quiz
class QuizApiView(generics.RetrieveAPIView):
    serializer_class = QuizSerializer
    lookup_url_kwarg = 'pk'

    def get_queryset(self):
        pk = self.kwargs.get(self.lookup_url_kwarg)
        return Quiz.objects.filter(id=pk)

    # def get_object(self, queryset=None):
    #     print(self.kwargs['pk'])
    #     return Quiz.objects.filter(id=self.kwargs['pk'])

    # queryset = Quiz.objects.all()


class QuestionApiViewList(generics.ListAPIView):
    serializer_class = QuestionSerializer
    lookup_url_kwarg = 'pk'

    def get_queryset(self):
        pk = self.kwargs.get(self.lookup_url_kwarg)
        return Question.objects.filter(quiz__id=pk)


# class AnswerApiView(generics.CreateAPIView, generics.RetrieveUpdateDestroyAPIView):
class AnswerApiView(APIView):
    def get(self, request, *args, **kwargs):
        print(request.data['pk'])
    надо настроить slug, а то конфликтуют pk
    можно посмотреть, что делает ModelViewSet, он вроде гибкий
    в любом случае надо разные посмотреть и выбрать адекватные
        pass

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
