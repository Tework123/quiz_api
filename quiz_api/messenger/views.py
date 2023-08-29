from django.db.models import Q
from rest_framework.generics import ListAPIView, RetrieveAPIView

from messenger.models import Chat, Relationship, Message
from messenger.serializers import ChatListSerializer, DialogListSerializer, \
    MessageListSerializer, ChatMessageListSerializer


class ChatList(ListAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatListSerializer
    # get показывает все чаты
    # post создает новый чат
    # put обновляет название чата, может, добавляет человека в чат
    # delete удалить чат по pk


class ChatMessageList(ListAPIView):
    serializer_class = ChatMessageListSerializer

    # get показывает все сообщения
    # post создает новое сообщение в этот чат(по pk)
    # put изменяет сообщение в этом чате(чат по pk), сообщение по id наверное, также фото можно изменить
    # или удалить?
    # delete удалить сообщение по id

    # сначала попробовать готовые миксины, если не получится - с нуля через apiview

    def get_queryset(self):
        return Message.objects.filter(chat__pk=self.kwargs['pk']).order_by('-data_create')


class DialogList(ListAPIView):
    serializer_class = DialogListSerializer

    def get_queryset(self):
        user = self.request.user
        return Relationship.objects.filter(Q(user_1=user) | Q(user_2=user))


class MessageList(ListAPIView):
    serializer_class = MessageListSerializer

    def get_queryset(self):
        return Message.objects.filter(relationship__pk=self.kwargs['pk']).order_by('-data_create')
