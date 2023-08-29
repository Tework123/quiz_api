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
        fields = '__all__'


class DialogListSerializer(ModelSerializer):
    class Meta:
        model = Relationship
        fields = '__all__'


class MessageListSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
