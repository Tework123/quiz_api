from django.urls import path
from messenger.views import ChatList, DialogList, MessageList, ChatMessageList, ChatDetail

urlpatterns = [
    #
    path('chats/', ChatList.as_view()),
    path('chats/<int:pk>/', ChatDetail.as_view()),
    path('chats/messages/<int:pk>/', ChatMessageList.as_view()),
    path('chats/messages/<int:pk>/<int:id>/', ChatMessageList.as_view()),

    # path('statistics/<slug:slug>/', QuizDetailStatistics.as_view()),
    path('dialogs/', DialogList.as_view()),
    path('dialogs/<int:pk>/', MessageList.as_view())

]
