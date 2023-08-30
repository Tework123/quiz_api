from django.contrib.auth.models import User
from django.db import models


class Relationship(models.Model):
    user_1 = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_1')
    user_2 = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_2')
    status = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.user_1}, {self.user_2}'


class Chat(models.Model):
    name = models.CharField(max_length=100)
    close = models.BooleanField(default=False)
    user = models.ManyToManyField(User)

    def __str__(self):
        return f'{self.name}'


class Image(models.Model):
    file = models.ImageField(upload_to='image/')

    def __str__(self):
        return f'{self.file}'


class Message(models.Model):
    text = models.TextField(max_length=1000)
    attachment = models.ManyToManyField(Image, blank=True)

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, null=True, blank=True)
    relationship = models.ForeignKey(Relationship, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    data_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk}. {self.user}, {self.text}'
