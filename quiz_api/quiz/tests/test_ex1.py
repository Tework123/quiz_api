import random

import pytest
from django.contrib.auth.models import User, Permission, Group
from django.urls import reverse
from django.utils import timezone
from faker import Faker

from quiz.models import Quiz, Answer, ResultAnswer, Question


@pytest.fixture()
def create_db():
    User.objects.create_superuser(email='admin@mail.ru',
                                  username='admin',
                                  password='admin')

    User.objects.create_user(email='user@mail.ru',
                             username='user',
                             password='user')

    # добавляем необходимые права для групп
    permissions = Permission.objects.filter(
        name__in=['Can view answer', 'Can view question',
                  'Can view quiz', 'Can add result answer',
                  'Can change result answer', 'Can delete result answer',
                  'Can view result answer'])

    # добавляем группы, а также разрешения
    groups = ['developers', 'designs', 'QA', 'managers', 'quest']
    groups_objects = []
    for one_group in groups:
        group = Group.objects.create(name=one_group)
        groups_objects.append(group)
        for perm in permissions:
            group.permissions.add(perm)

    # добавляем пользователей
    fake = Faker()
    count_users = 5
    count_questions = 5
    count_answers = 10
    count_users_answers = 10

    user_objects = []
    for i in range(count_users):
        name = fake.name()
        name_join = name.replace(' ', '')

        user = User.objects.create_user(email=name_join + '@mail.ru',
                                        username=name_join, password=name_join)

        # добавляем пользователей в группы
        user.groups.add(random.choice(groups_objects))
        user_objects.append(user)

    # добавляем опросы
    few_quiz = ['dota', 'cs', 'warcraft', 'legomen', 'tresh']
    quiz_objects = []
    for one_quiz in few_quiz:
        quiz = Quiz.objects.create(name=one_quiz, slug=one_quiz,
                                   date_stop=timezone.now(),
                                   description=fake.text(),
                                   creator_id=1)

        # добавляем к опросу группы, для которых он предназначен
        quiz.group.add(random.choice(groups_objects))
        quiz_objects.append(quiz)

    # добавляем вопросы
    question_objects = []
    for i in range(count_questions):
        question = Question.objects.create(description=fake.text(),
                                           quiz=random.choice(quiz_objects))
        question_objects.append(question)

    # добавляем ответы
    answer_objects = []
    for i in range(count_answers):
        answer = Answer.objects.create(description=fake.text(),
                                       question=random.choice(question_objects))
        answer_objects.append(answer)

    # добавляем ответы пользователей
    for i in range(count_users_answers):
        ResultAnswer.objects.create(user=random.choice(user_objects),
                                    answer=random.choice(answer_objects))


@pytest.fixture(scope='function')
def login_user(client, create_db):
    client.login(username='user', password='user')


@pytest.fixture(scope='function')
def login_admin(client, create_db):
    client.login(username='admin', password='admin')


@pytest.mark.django_db
def test_get_request(client, create_db, login_user):
    response = client.get('/api/v1/quiz/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_request2(client, create_db, login_admin):
    # assert User.objects.count() == 1
    # не работает
    # ошибка не с выходом, просто ошибка
    response = client.get('/api/v1/quiz/statistics/')
    assert response.status_code == 200
