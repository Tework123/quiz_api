from django.urls import path

from quiz.views import (QuizList, QuizDetail, QuestionList,
                        AddAnswer, QuizListStatistics, QuizDetailStatistics, CreateQuiz, CreateQuestion, CreateAnswer,
                        UpdateQuestion, UpdateAnswer, UpdateQuiz)

urlpatterns = [
    # вывод статистики
    path('statistics/', QuizListStatistics.as_view()),
    path('statistics/<slug:slug>/', QuizDetailStatistics.as_view()),

    # создание опросов
    path('create_quiz/', CreateQuiz.as_view()),
    path('update_quiz/<slug:slug>/', UpdateQuiz.as_view()),

    path('create_question/<slug:slug>/', CreateQuestion.as_view()),
    path('update_question/<slug:slug>/<int:pk>/', UpdateQuestion.as_view()),

    path('create_answer/<int:pk>/', CreateAnswer.as_view()),
    path('update_answer/<int:pk>/', UpdateAnswer.as_view()),

    # показывает опросы
    path('', QuizList.as_view()),
    path('<slug:slug>/', QuizDetail.as_view()),
    path('<slug:slug>/questions/', QuestionList.as_view()),
    path('<slug:slug>/questions/<int:pk>/', AddAnswer.as_view()),
]
