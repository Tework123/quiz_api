import random
from django.contrib.auth.models import User, Permission, Group
from django.core.management import BaseCommand
from django.utils import timezone
from faker import Faker
from quiz.models import Quiz, Question, Answer, ResultAnswer


class Command(BaseCommand):

    def add_arguments(self, parser):
        info_for_help = ' Впишите цифры в таком порядке:'
        ' Пользователи, вопросы, ответы, ответы пользователей'

        parser.add_argument('count_users', type=int,
                            help='Сколько нужно пользователей?' + info_for_help)
        parser.add_argument('count_questions', type=int,
                            help='Сколько нужно вопросов?' + info_for_help)
        parser.add_argument('count_answers', type=int,
                            help='Сколько нужно ответов?' + info_for_help)
        parser.add_argument('count_users_answers', type=int,
                            help='Сколько нужно ответов пользователей?' + info_for_help)

    def handle(self, *args, **kwargs):
        fake = Faker()
        count_users = kwargs['count_users']
        count_questions = kwargs['count_questions']
        count_answers = kwargs['count_answers']
        count_users_answers = kwargs['count_users_answers']

        print(count_users, count_questions, count_answers, count_users_answers)

        # добавляем необходимые права для групп
        permissions = Permission.objects.filter(
            name__in=['Can view answer', 'Can view question',
                      'Can view quiz', 'Can add result answer',
                      'Can change result answer', 'Can delete result answer',
                      'Can view result answer'])

        self.stdout.write(self.style.HTTP_NOT_MODIFIED('Права для групп добавлены'))

        # добавляем группы, а также разрешения
        groups = ['developers', 'designs', 'QA', 'managers', 'quest']
        groups_objects = []
        for one_group in groups:
            group = Group.objects.create(name=one_group)
            groups_objects.append(group)
            for perm in permissions:
                group.permissions.add(perm)

        self.stdout.write(self.style.HTTP_NOT_MODIFIED('Группы добавлены'))

        # добавляем админа
        User.objects.create_superuser(email='admin@mail.ru',
                                      username='admin',
                                      password='admin')

        self.stdout.write(self.style.HTTP_NOT_MODIFIED('Админ добавлен'))

        # добавляем пользователей
        user_objects = []
        for i in range(count_users):
            name = fake.name()
            name_join = name.replace(' ', '')

            user = User.objects.create_user(email=name_join + '@mail.ru',
                                            username=name, password=name_join)

            # добавляем пользователей в группы
            user.groups.add(random.choice(groups_objects))
            user_objects.append(user)

        self.stdout.write(self.style.HTTP_NOT_MODIFIED('Пользователи добавлены'))

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

        self.stdout.write(self.style.HTTP_NOT_MODIFIED('Опросы добавлены'))

        # добавляем вопросы
        question_objects = []
        for i in range(count_questions):
            question = Question.objects.create(description=fake.text(),
                                               quiz=random.choice(quiz_objects))
            question_objects.append(question)

        self.stdout.write(self.style.HTTP_NOT_MODIFIED('Вопросы добавлены'))

        # добавляем ответы
        answer_objects = []
        for i in range(count_answers):
            answer = Answer.objects.create(description=fake.text(),
                                           question=random.choice(question_objects))
            answer_objects.append(answer)

        self.stdout.write(self.style.HTTP_NOT_MODIFIED('Ответы добавлены'))

        # добавляем ответы пользователей
        for i in range(count_users_answers):
            ResultAnswer.objects.create(user=random.choice(user_objects),
                                        answer=random.choice(answer_objects))

        self.stdout.write(self.style.HTTP_NOT_MODIFIED('Ответы пользователей добавлены'))
        self.stdout.write(self.style.SUCCESS('База данных успешно создана!'))
