import pytest
from django.urls import reverse

from quiz.models import Quiz


@pytest.mark.urls('quiz_api.quiz')
def test_view(client):
    url = reverse('api/v1/quiz/')
    response = client.get(url)
    assert response.status_code == 200
