from django.urls import path

from quiz.views import QuizApiViewList, QuestionApiViewList, QuizApiView, AnswerApiView

urlpatterns = [
    path('', QuizApiViewList.as_view()),
    path('<int:pk>', QuizApiView.as_view()),
    path('<int:pk>/questions', QuestionApiViewList.as_view()),
    path('<int:pk>/questions/<int:id>', AnswerApiView.as_view())

]
