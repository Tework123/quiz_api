from django.db.models import Q
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, \
    ListCreateAPIView
from rest_framework.response import Response

from messenger.models import Chat, Relationship, Message
from messenger.serializers import ChatListSerializer, DialogListSerializer, \
    MessageListSerializer, ChatMessageListSerializer


class ChatList(ListCreateAPIView):
    serializer_class = ChatListSerializer

    def get_queryset(self):
        return Chat.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            close_field = request.data['close']
            close = True
        except:
            close = False
        chat = Chat.objects.create(name=request.data['name'],
                                   close=close)

        for user in request.data.getlist('user'):
            chat.user.add(user)
        return Response('Беседа создана успешно')


class ChatDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = ChatListSerializer

    def get_queryset(self):
        return Chat.objects.filter(pk=self.kwargs['pk'])

    def update(self, request, *args, **kwargs):
        chat = Chat.objects.filter(pk=self.kwargs['pk'])

        try:
            close_field = request.data['close']
            close = True
        except:
            close = False

        chat.update(name=request.data['name'],
                    close=close)

        for user in request.data.getlist('user'):
            chat[0].user.add(user)

        return Response('Беседа обновлена успешно')

    def delete(self, request, *args, **kwargs):
        Chat.objects.get(pk=kwargs['pk']).delete()
        return Response('Беседа удалена успешно')


class ChatMessageList(ListCreateAPIView):
    serializer_class = ChatMessageListSerializer

    # get показывает все сообщения
    # post создает новое сообщение в этот чат(по pk)
    # put изменяет сообщение в этом чате(чат по pk), сообщение по id наверное, также фото можно изменить
    # или удалить?
    # delete удалить сообщение по id

    def get_queryset(self):
        return Message.objects.filter(chat__pk=self.kwargs['pk']).order_by('-data_create')

    def create(self, request, *args, **kwargs):
        # добавить chat или relationship, attachment(image)
        # нужна доп проверка

        message = Message.objects.create(text=request.data['text'],
                                         user=self.request.user,
                                         )

        for attachment in request.data.getlist('attachment'):
            message.user.add(attachment)
        return Response('Сообщение создано успешно')


class ChatMessageDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = ChatMessageListSerializer

    # нужно добавить везде permissions классы собственные
    # нужно проверить на наличие данного чата у юзера

    def get_queryset(self):
        return Message.objects.filter(id=self.kwargs['id'])

    def update(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass


class DialogList(ListAPIView):
    serializer_class = DialogListSerializer

    def get_queryset(self):
        user = self.request.user
        return Relationship.objects.filter(Q(user_1=user) | Q(user_2=user))


class MessageList(ListAPIView):
    serializer_class = MessageListSerializer

    def get_queryset(self):
        return Message.objects.filter(relationship__pk=self.kwargs['pk']).order_by('-data_create')
