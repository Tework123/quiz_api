from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from quiz.models import Quiz
from quiz.serializer import QuizSerializer


class QuizApiViewList(generics.ListAPIView):
    serializer_class = QuizSerializer

    def get_queryset(self):
        print(self.request.user)
        return Quiz.objects.all()


# class QuizApiViewList(APIView):
#     def get(self, request):
#         print(self.request.user)
#
#         quiz = Quiz.objects.all()
#         return Response({'quiz': quiz})
