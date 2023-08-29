from django.urls import path
from messenger.views import ChatList, DialogList, MessageList, ChatMessageList

urlpatterns = [
    #
    path('chats/', ChatList.as_view()),
    path('chats/<int:pk>/', ChatMessageList.as_view()),

    # path('statistics/<slug:slug>/', QuizDetailStatistics.as_view()),
    path('dialogs/', DialogList.as_view()),
    path('dialogs/<int:pk>/', MessageList.as_view())

]
