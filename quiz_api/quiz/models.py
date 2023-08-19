from django.contrib.auth.models import User, Group
from django.db import models


class Quiz(models.Model):
    name = models.CharField(max_length=100)
    date_start = models.DateTimeField(auto_now_add=True)
    date_stop = models.DateTimeField(null=True)
    description = models.TextField(blank=True)
    creator = models.ForeignKey(User, on_delete=models.PROTECT)

    # так как он видит двух user добавляем другое имя
    # consumer = models.ManyToManyField(User, related_name='consumer')

    # для добавления только определенных групп людей для опроса
    group = models.ManyToManyField(Group)

    def __str__(self):
        return self.name


class Question(models.Model):
    description = models.TextField(blank=True, max_length=500)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.description


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class ResultAnswer(models.Model):
    result = models.IntegerField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
