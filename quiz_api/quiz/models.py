from django.contrib.auth.models import User, Group
from django.db import models
from django.urls import reverse


class Quiz(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL", null=True)
    date_start = models.DateTimeField(auto_now_add=True)
    date_stop = models.DateTimeField(null=True)
    description = models.TextField(blank=False)
    creator = models.ForeignKey(User, on_delete=models.PROTECT)

    # так как он видит двух user добавляем другое имя
    # consumer = models.ManyToManyField(User, related_name='consumer')

    # для добавления только определенных групп людей для опроса
    group = models.ManyToManyField(Group)

    def __str__(self):
        return self.name


class Question(models.Model):
    description = models.TextField(blank=False, max_length=500)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.description


class Answer(models.Model):
    description = models.TextField(blank=True, max_length=500)
    question = models.ForeignKey(Question, related_name='answer_list', on_delete=models.CASCADE)

    def __str__(self):
        return self.description


class ResultAnswer(models.Model):
    user = models.ForeignKey(User, related_name='user',  on_delete=models.CASCADE, null=True)
    answer = models.ForeignKey(Answer, related_name='result_answer_list', on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.answer