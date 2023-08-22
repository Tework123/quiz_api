from django.urls import path

from quiz.views import QuizList, QuizDetail, QuestionList, AddAnswer, QuizListStatistics, QuizDetailStatistics

urlpatterns = [
    path('', QuizList.as_view()),

    path('statistics/', QuizListStatistics.as_view()),
    path('statistics/<slug:slug>/', QuizDetailStatistics.as_view()),

    path('<slug:slug>/', QuizDetail.as_view()),
    path('<slug:slug>/questions', QuestionList.as_view()),
    path('<slug:slug>/questions/<int:pk>', AddAnswer.as_view()),
]
