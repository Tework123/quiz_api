from django.db.models import Count
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from quiz.models import Quiz, Question, ResultAnswer
from quiz.serializers import (QuizListSerializer, QuizDetailSerializer,
                              QuestionListSerializerThird,
                              QuizListStatisticsSerializer, QuizDetailStatisticsSerializer)


# ''
# показывает все опросы
class QuizList(ListAPIView):
    serializer_class = QuizListSerializer

    def get_queryset(self):
        return Quiz.objects.all()


# <slug:slug>/
# показывает информация о конкретном опросе
class QuizDetail(RetrieveAPIView):
    serializer_class = QuizDetailSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        slug = self.kwargs.get(self.lookup_field)
        return Quiz.objects.filter(slug=slug)


# <slug:slug>/questions
# показывает все вопросы, вместе с ответами конкретного пользователя
class QuestionList(ListAPIView):
    serializer_class = QuestionListSerializerThird
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]

    # добавляем в начало возвращаемого из сериализатора списка user_id
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data.insert(0, {'user_id': self.request.user.id})
        return response

    def get_queryset(self):
        slug = self.kwargs.get(self.lookup_field)
        return Question.objects.filter(quiz__slug=slug)


# <slug:slug>/questions/<int:pk>
# добавляет ответы пользователя
class AddAnswer(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        old_answer = ResultAnswer.objects.filter(user=self.request.user, answer_id=kwargs['pk'])
        if old_answer:
            return Response({'old_answer': 'Вы уже выбрали этот ответ'})

        # достаем вопрос к которому принадлежит id выбранного ответа
        question = Question.objects.get(answer_list=1)

        # по id вопроса достаем все уже раннее сделанные ответы на этот вопрос и удаляем их
        ResultAnswer.objects.filter(answer__question=question.id,
                                    user_id=self.request.user.id).delete()

        # создаем новый ответ, user - тот, кто проходит тест,
        # answer_id - id ответа, на который он нажал
        ResultAnswer.objects.create(user=self.request.user, answer_id=kwargs['pk'])
        return Response({'new_answer': 'hello'})


# statistics/
# показывает статистику по всем опросам
class QuizListStatistics(ListAPIView):
    serializer_class = QuizListStatisticsSerializer

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        # считает количество уникальных пользователей,
        # которые ответили хотя бы на один вопрос в quiz и группирует по quiz
        response = Quiz.objects.annotate(
            questions=Count('question__answer_list__result_answer_list__user', distinct=True))
        return response


# statistics/<slug:slug>/
# показывает статистику с процентами на каждый ответ в каждом вопросе,
# выводит все вопросы выбранного опроса
class QuizDetailStatistics(ListAPIView):
    serializer_class = QuizDetailStatisticsSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        slug = self.kwargs.get(self.lookup_field)

        response = Question.objects.filter(quiz__slug=slug)
        return response

dasdasd