from rest_framework.serializers import ModelSerializer

from messenger.models import Chat, Relationship, Message
from quiz.models import Quiz


class ChatListSerializer(ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'


class ChatDetailSerializer(ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'


class ChatMessageListSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'text', 'attachment', 'user', ]


class ChatMessageDetailSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'text', 'attachment']


class DialogListSerializer(ModelSerializer):
    class Meta:
        model = Relationship
        fields = ['id', 'user_2', 'status']


class DialogMessageListSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
