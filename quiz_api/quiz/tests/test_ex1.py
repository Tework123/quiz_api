import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from faker import Faker

fake = Faker()


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url, slug, status', [
        ('quiz', 'dota', 200),
        ('quiz', 'warcraft', 200),
    ]
)
def test_get_request(client, create_db, login_user, url, slug, status):
    response = client.get(f'/api/v1/{url}/{slug}/')
    assert response.status_code == status
    assert response.json() == response.json()


@pytest.mark.django_db
def test_get_request3(client, create_db, login_admin):
    response = client.get('/api/v1/quiz/statistics/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_request2(client, create_db, login_user):
    response = client.get('/api/v1/quiz/dota/questions/1/')
    assert response.status_code == 403
    assert response.json() == {'detail': 'You do not have permission to perform this action.'}


@pytest.mark.django_db
def test_get_request24(client, create_db, login_admin):
    admin = User.objects.get(username='admin')
    data = {'name': 'one_quiz', 'slug': 'one_quiz',
            'date_stop': timezone.now(),
            'description': fake.text(),
            'creator': admin}

    response = client.post('/api/v1/quiz/create_quiz/', data=data)
    assert response.status_code == 200
    assert response.json() == 'Опрос создан успешно'
