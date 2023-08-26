from django.contrib.auth.models import Group
from django.db.models import Count
from rest_framework.generics import RetrieveAPIView, ListAPIView, ListCreateAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from quiz.models import Quiz, Question, ResultAnswer, Answer
from quiz.permissions import IsGroup
from quiz.serializers import (QuizListSerializer, QuizDetailSerializer,
                              QuestionListSerializerThird,
                              QuizListStatisticsSerializer, QuizDetailStatisticsSerializer,
                              CreateQuizSerializer,
                              CreateQuestionSerializer, CreateAnswerSerializer)


# ''
# показывает все опросы
class QuizList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuizListSerializer

    def get_queryset(self):
        return Quiz.objects.all()


# <slug:slug>/
# показывает информацию о конкретном опросе
class QuizDetail(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuizDetailSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        slug = self.kwargs.get(self.lookup_field)
        return Quiz.objects.filter(slug=slug)


# <slug:slug>/questions
# показывает все вопросы, вместе с ответами конкретного пользователя
class QuestionList(ListAPIView):
    permission_classes = [IsAuthenticated, IsGroup]
    serializer_class = QuestionListSerializerThird
    lookup_field = 'slug'

    # добавляем в начало возвращаемого из сериализатора списка user_id
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data.insert(0, {'user_id': self.request.user.id})
        return response

    def get_queryset(self):
        slug = self.kwargs.get(self.lookup_field)

        return Question.objects.filter(quiz__slug=slug)


# <slug:slug>/questions/<int:pk>w
# добавляет ответы пользователя
class AddAnswer(APIView):
    permission_classes = [IsAuthenticated, IsGroup]

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

    permission_classes = [IsAdminUser]

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
    permission_classes = [IsAdminUser]
    serializer_class = QuizDetailStatisticsSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        slug = self.kwargs.get(self.lookup_field)

        response = Question.objects.filter(quiz__slug=slug)
        return response


# create_quiz/
# создает опрос(как админка)
class CreateQuiz(ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Quiz.objects.all()
    serializer_class = CreateQuizSerializer

    def create(self, request, *args, **kwargs):
        quiz = Quiz.objects.create(name=request.data['name'],
                                   slug=request.data['slug'],
                                   date_stop=request.data['date_stop'],
                                   description=request.data['description'],
                                   creator=self.request.user)

        for group in request.data.getlist('group'):
            quiz.group.add(group)
            # group = Group.objects.get(id=self.request.data['group'])
        return Response('Опрос создан успешно')


# update_quiz/<slug:slug>/
# обновляет опрос(как админка)
class UpdateQuiz(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CreateQuizSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        slug = self.kwargs.get(self.lookup_field)
        return Quiz.objects.filter(slug=slug)

    def update(self, request, *args, **kwargs):
        slug = self.kwargs.get(self.lookup_field)

        Quiz.objects.filter(slug=slug).update(name=self.request.data['name'],
                                              slug=self.request.data['slug'],
                                              date_stop=self.request.data['date_stop'],
                                              description=self.request.data['description'],
                                              )

        # для обновления поля many_to_many
        # мы меняем доступные группы для теста, достаем нужный quiz, введенную группу
        # и используем add
        quiz = Quiz.objects.get(slug=self.request.data['slug'])
        groups = request.data.getlist('group')
        for group in groups:
            quiz.group.add(group)

        return Response({'data': 'Опрос изменен успешно'})

    def delete(self, request, *args, **kwargs):
        slug = self.kwargs.get(self.lookup_field)
        Quiz.objects.filter(slug=slug).delete()
        return Response({'data': 'Опрос удален успешно'})


# create_question/<slug:slug>/
# создает вопрос(как админка)
class CreateQuestion(ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CreateQuestionSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        slug = self.kwargs.get(self.lookup_field)
        return Question.objects.filter(quiz__slug=slug)

    def create(self, request, *args, **kwargs):
        slug = self.kwargs.get(self.lookup_field)
        quiz_object = Quiz.objects.get(slug=slug)
        Question.objects.create(description=request.data['description'], quiz=quiz_object)
        return Response('Вопрос создан успешно')


# update_question/<slug:slug>/<int:pk>/
# обновляет вопрос(как админка)
class UpdateQuestion(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CreateQuestionSerializer

    def get_queryset(self):
        return Question.objects.filter(pk=self.kwargs['pk'])

    def update(self, request, *args, **kwargs):
        (Question.objects.filter(pk=self.kwargs['pk'])
         .update(description=self.request.data['description']))
        return Response({'data': 'Вопрос изменен успешно'})

    def delete(self, request, *args, **kwargs):
        Question.objects.filter(pk=self.kwargs['pk']).delete()
        return Response({'data': 'Вопрос удален успешно'})


# create_answer/<int:pk>/
# создает ответ(как админка)
class CreateAnswer(ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CreateAnswerSerializer

    def get_queryset(self):
        return Answer.objects.filter(question__pk=self.kwargs['pk'])

    def create(self, request, *args, **kwargs):
        question_object = Question.objects.get(pk=self.kwargs['pk'])
        Answer.objects.create(description=request.data['description'], question=question_object)
        return Response('Ответ создан успешно')


# update_answer/<int:pk>/
# обновляет ответ(как админка)
class UpdateAnswer(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CreateAnswerSerializer

    def get_queryset(self):
        return Answer.objects.filter(pk=self.kwargs['pk'])

    def update(self, request, *args, **kwargs):
        (Answer.objects.filter(pk=self.kwargs['pk'])
         .update(description=self.request.data['description']))
        return Response({'data': 'Ответ изменен успешно'})

    def delete(self, request, *args, **kwargs):
        Answer.objects.filter(pk=self.kwargs['pk']).delete()
        return Response({'data': 'Ответ удален успешно'})
