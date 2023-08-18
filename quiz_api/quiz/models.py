from django.contrib.auth.models import User
from django.db import models


class Quiz(models.Model):
    name = models.CharField(max_length=100)
    date_start = models.DateTimeField(auto_now_add=True)
    date_stop = models.DateTimeField(null=True)
    description = models.TextField(blank=True)
    creator = models.ForeignKey(User, on_delete=models.PROTECT)

    # так как он видит двух user добавляем другое имя
    consumer = models.ManyToManyField(User, related_name='consumer')


class Question(models.Model):
    description = models.TextField(blank=True, max_length=500)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)


class Answer(models.Model):
    description = models.TextField(blank=True, max_length=500)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class ResultAnswer(models.Model):
    result = models.IntegerField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)




