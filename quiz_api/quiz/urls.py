from django.urls import path

from quiz.views import QuizApiViewList
urlpatterns = [
    path('', QuizApiViewList.as_view()),
    # path('', QuizApiViewList.as_view()),

]