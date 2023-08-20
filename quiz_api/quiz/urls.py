from django.urls import path

from quiz.views import QuizApiViewList, QuestionApiViewList, QuizApiView, AnswerApiView

urlpatterns = [
    path('', QuizApiViewList.as_view()),
    path('<slug:slug>/', QuizApiView.as_view()),
    path('<slug:slug>/questions', QuestionApiViewList.as_view()),
    path('<slug:slug>/questions/<int:pk>', AnswerApiView.as_view())
]
