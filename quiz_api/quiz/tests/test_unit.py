from unittest import TestCase
from django.contrib.auth.models import User
from django.core import management


class TestClass(TestCase):
    # не работает
    def setUp(self):
        management.call_command('migrate')
        management.call_command('flush')
#
#     def tearDown(self):
#         management.call_command('migrate')
#         management.call_command('flush')


class UserModelTest(TestCase):
    # это перед каждым тестом, а надо один раз за сессию
    # def setUp(self):
    #     management.call_command('migrate')
    #     management.call_command('flush')

    def test_first_name_label(self):
        user = User.objects.create_user(email='user@mail.ru',
                                        username='user',
                                        password='user')
        user.save()
        user = User.objects.get(id=1)
        email = user.email
        self.assertEqual(email, 'user@mail.ru')

    def test_date_of_death_label(self):
        username = User.objects.get(id=1)
        username = username.username
        self.assertEqual(username, 'user')

#
# class AuthorListViewTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # Create 13 authors for pagination tests
#         number_of_authors = 13
#
#         for author_id in range(number_of_authors):
#             Author.objects.create(
#                 first_name=f'Dominique {author_id}',
#                 last_name=f'Surname {author_id}',
#             )
#
#     def test_view_url_exists_at_desired_location(self):
#         response = self.client.get('/catalog/authors/')
#         self.assertEqual(response.status_code, 200)
#
#     def test_view_url_accessible_by_name(self):
#         response = self.client.get(reverse('authors'))
#         self.assertEqual(response.status_code, 200)
#
#     def test_view_uses_correct_template(self):
#         response = self.client.get(reverse('authors'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'catalog/author_list.html')
#
#     def test_pagination_is_ten(self):
#         response = self.client.get(reverse('authors'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTrue('is_paginated' in response.context)
#         self.assertTrue(response.context['is_paginated'] == True)
#         self.assertEqual(len(response.context['author_list']), 10)
#
#     def test_lists_all_authors(self):
#         # Get second page and confirm it has (exactly) remaining 3 items
#         response = self.client.get(reverse('authors')+'?page=2')
#         self.assertEqual(response.status_code, 200)
#         self.assertTrue('is_paginated' in response.context)
#         self.assertTrue(response.context['is_paginated'] == True)
#         self.assertEqual(len(response.context['author_list']), 3)
