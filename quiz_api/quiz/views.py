from django.contrib.auth.models import User
from django.contrib.postgres.aggregates import StringAgg
from django.db.models import CharField, Q
from django.db.models.functions import Cast
from django.shortcuts import render
from rest_framework import generics
from rest_framework.generics import RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from quiz.models import Quiz, Question, Answer, ResultAnswer
from quiz.serializers import QuizListSerializer, QuizSerializer, \
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

    # добавляем в начало возвращаемого из сериализатора списка user_id
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data.insert(0, {'user_id': self.request.user.id})

        # фронт берет этот user_id и прокручивает циклы таким образом:
        # for questions in response.data:
        #     for question in questions.items():
        #         if question[0] == 'description' or question[0] == 'id':
        #             print(f'question_info: {question[1]}')
        #         for answers in question:
        #             if type(answers) == list:
        #                 for answer in answers:
        #                     print(f'answer_id: {answer["id"]}')
        #                     print(f'answer_description: {answer["description"]}')
        #                     for user in answer['result_answer_list']:
        #                         if user['user_id'] == self.request.user.id:
        #                             print('Отмечаю тебя красненьким')
        #                         print(f'user_id: {user["user_id"]}')
        #     print('_________________________________')

        return response

    def get_queryset(self):
        slug = self.kwargs.get(self.lookup_field)
        user = self.request.user
        return Question.objects.filter(quiz__slug=slug)


#     можно посмотреть, что делает ModelViewSet, он вроде гибкий
#     в любом случае надо разные посмотреть и выбрать адекватные

class AnswerApiView(CreateAPIView, DestroyAPIView, UpdateAPIView):
    serializer_class = AnswerGetSerializer

    # lookup_field = 'slug'

    def get_queryset(self):
        slug = self.kwargs.get(self.lookup_field)
        user = self.request.user
        return Question.objects.filter(quiz__slug=slug)

    def create(self, request, *args, **kwargs):
        old_answer = ResultAnswer.objects.filter(user=self.request.user, answer_id=kwargs['pk'])
        if old_answer:
            return Response({'old_answer': 'Вы уже выбрали этот ответ'})

        new_answer = ResultAnswer.objects.create(user=self.request.user, answer_id=kwargs['pk'])
        return Response({'new_answer': 'hello'})

    def update(self, request, *args, **kwargs):
        print('update poimal')
        print(request.data)
        print(args)
        print(kwargs['pk'])
        current_question = Question.objects.filter(answer_list=1)
        print(current_question)
        whole_answer_on_this_question = Answer.objects.filter(question=current_question[0])
        print(whole_answer_on_this_question)

        whole_my_answer = ResultAnswer.objects.filter(answer__in=whole_answer_on_this_question)
        print(whole_my_answer)
        # надо с помощью одного запроса вытащить по answer_id все ответы на вопрос,
        # принадлежащий этому ответу,
        # на который мы шлем запрос, чтобы его изменить,
        # (pk который). Далее у этих ответов надо вытащить все ответы данные этим пользователем
        # на эти ответы, удалить их, а тот, на который запрос отправился - записать в базу. Пока так.
        return Response({'change_answer': 'hello2'})

#
# # class AnswerApiView(generics.CreateAPIView, generics.RetrieveUpdateDestroyAPIView):
# class AnswerApiView(APIView):
#     def get(self, request, *args, **kwargs):
#         print(kwargs['pk'])
#         pk = kwargs['pk']
#         answer = Answer.objects.filter(pk=pk)
#         print(answer)
#         serializer = AnswerGetSerializer(answer, many=True)
#
#         return Response({'new_answer': serializer.data})
#
#     def post(self, request, *args, **kwargs):
#         print(request.data['id'])
#         id = request.data['id']
#
#         answer = Answer.objects.create(question_id=id)
#         return Response({'new_answer': AnswerSerializer(answer).data})

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
