from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.response import Response


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = (User.objects.create_user(email=validated_data['email'], username=validated_data['username'],
                                         password=validated_data['password']))
        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
