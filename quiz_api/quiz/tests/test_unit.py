from django.test import TestCase
from django.contrib.auth.models import User
from django.core import management
from faker import Faker

from messenger.models import Chat

fake = Faker()


class UserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(email="user@mail.ru", username="user@mail.ru", password="user@mail.ru" * 2)

        for i in range(10):
            name = fake.name()
            User.objects.create_user(email=name + "@mail.ru", username=name, password=name * 2)

    def test_count_users(self):
        count_users = User.objects.all().count()

        self.assertEqual(count_users, 11)


class UserModel2Test(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        User.objects.create_user(email='user@mail.ru',
                                 username='user',
                                 password='user')

    def setUp(self) -> None:
        """логиним юзера перед каждым запросом"""
        self.client.login(username='user', password='user')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/api/v1/messenger/chats/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_exists_at_desired_location1(self):
        response = self.client.get('/api/v1/messenger/chats/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_exists_at_desired_location2(self):
        response = self.client.post('/api/v1/messenger/chats/', {'name': 'new_chat', 'close': True})
        self.assertEqual(response.status_code, 200)

        chat = Chat.objects.all()
        print(chat)
        self.assertEqual(chat.count(), 1)
