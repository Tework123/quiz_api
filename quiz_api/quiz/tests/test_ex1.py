import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from quiz.models import Quiz


# @pytest.fixture(scope='session')
# def fixture_1():
#     print('start test')
#     yield 5
#     print('end test')
#
#
# def test_view1(fixture_1):
#     print('11111111')
#     assert fixture_1 == 1
#
#
# def test_view2(fixture_1):
#     print('2222222')
#     assert fixture_1 == 1


# def test_user_create(user_1):
#     print(user_1)
#     User.objects.create_user('test', 'test@test.com', 'test')
#     assert User.objects.count() == 1
#
#
# def test_user_create1(user_1):
#     print(user_1)
#     # User.objects.create_user('test', 'test@test.com', 'test')
#     assert User.objects.count() == 1

@pytest.fixture()
def test_create_db(db):
    User.objects.create_superuser(email='admin@mail.ru',
                                  username='admin',
                                  password='admin')
    # можно сделать отдельную фикстуру, там прописать все данные, а дальше передавать в тесты


@pytest.mark.django_db
def test_get_request(client, test_create_db):
    assert User.objects.count() == 1

    response = client.get('/api/v1/quiz/')
    print(response.data)
    assert response.status_code == 200
