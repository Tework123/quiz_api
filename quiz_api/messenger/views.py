from django.db.models import Q
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, \
    ListCreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from messenger.models import Chat, Relationship, Message
from messenger.serializers import ChatListSerializer, DialogListSerializer, \
    ChatMessageListSerializer, ChatMessageDetailSerializer, DialogMessageListSerializer


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


class ChatMessageList(ModelViewSet):
    serializer_classes = {'list': ChatMessageListSerializer,
                          'create': ChatMessageDetailSerializer}

    default_serializer_class = ChatMessageListSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_queryset(self):
        return Message.objects.filter(chat__pk=self.kwargs['pk']).order_by('-data_create')

    def create(self, request, *args, **kwargs):
        message = Message.objects.create(text=request.data['text'],
                                         user=self.request.user,
                                         chat_id=kwargs['pk'],
                                         )

        for attachment in request.data.getlist('attachment'):
            message.attachment.add(attachment)
        return Response('Сообщение создано успешно')


class ChatMessageDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = ChatMessageDetailSerializer

    # нужно добавить везде permissions классы собственные
    # нужно проверить на наличие данного чата у юзера

    def get_queryset(self):
        return Message.objects.filter(pk=self.kwargs['pk'])

    def update(self, request, *args, **kwargs):
        message = Message.objects.filter(pk=kwargs['pk'])

        message.update(text=request.data['text'])

        # удаляем все прикрепленные many_to_many object
        message[0].attachment.clear()

        for attachment in request.data.getlist('attachment'):
            message[0].attachment.add(attachment)

        return Response('Сообщение изменено успешно')

    def delete(self, request, *args, **kwargs):
        Message.objects.get(pk=kwargs['pk']).delete()
        return Response('Сообщение удалено успешно')


class DialogList(ListCreateAPIView):
    serializer_class = DialogListSerializer

    # добавить друга(подписаться) - создается диалог,
    # но можно и без этого, просто написать сообщение человеку, в статусе будет = unknown

    def get_queryset(self):
        user = self.request.user
        return Relationship.objects.filter(Q(user_1=user) | Q(user_2=user))

    # вот тут вопрос, с фронта можно отправить post запрос при нажатии на кнопку 'добавить в друзья'?
    def create(self, request, *args, **kwargs):
        # проверка на существующую связь
        exist_relationship = Relationship.objects.get(Q(user_1=self.request.user, user_2=request.data['user_2']) |
                                                      Q(user_2=self.request.user, user_1=request.data['user_2']))

        if exist_relationship:
            return Response('Он уже связан с тобой')

        Relationship.objects.create(user_1=self.request.user,
                                    user_2_id=request.data['user_2'],
                                    status=request.data['status'])

        return Response('Отношения с пользователем установлены')


class DialogMessageList(RetrieveUpdateDestroyAPIView):
    serializer_class = DialogMessageListSerializer

    def get_queryset(self):
        return Message.objects.filter(relationship__pk=self.kwargs['pk']).order_by('-data_create')

    def update(self, request, *args, **kwargs):
        message = Message.objects.filter(pk=kwargs['pk'])

        message.update(text=request.data['text'])

        # удаляем все прикрепленные many_to_many object
        message[0].attachment.clear()

        for attachment in request.data.getlist('attachment'):
            message[0].attachment.add(attachment)

        return Response('Сообщение изменено успешно')

    def delete(self, request, *args, **kwargs):
        Message.objects.get(pk=kwargs['pk']).delete()
        return Response('Сообщение удалено успешно')
