from django.urls import path
from messenger.views import ChatList, DialogList, ChatMessageList, ChatDetail, ChatMessageDetail, \
    DialogMessageList

urlpatterns = [
    #
    path('chats/', ChatList.as_view()),
    path('chats/<int:pk>/', ChatDetail.as_view()),
    path('chats/messages/<int:pk>/', ChatMessageList.as_view({'get': 'list', 'post': 'create'})),
    path('chats/message/<int:pk>/', ChatMessageDetail.as_view()),

    # path('statistics/<slug:slug>/', QuizDetailStatistics.as_view()),
    path('dialogs/', DialogList.as_view()),
    # надо еще для изменения диалога url??
    path('dialogs/messages/<int:pk>/', DialogMessageList.as_view()),

]
