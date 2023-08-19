from django.urls import path

from register.views import CreateUserView

urlpatterns = [
    path('', CreateUserView.as_view()),

]
