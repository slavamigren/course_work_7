import copy

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from habits.models import Habit, NiceHabit


class UserTestCase(APITestCase):
    """Тест для контроллера UserCreateView"""

    def test_user_create(self):
        # Нового пользователя, заводить нужно только так, т.к. пароль шифруется
        # и просто созданный через create объект User не сможет авторизоваться
        userdata = {
            'email': 'test@test.ru',
            'password': '12345',
        }
        # создаём пользователя
        response = self.client.post(
            reverse('users:create_user'),
            data=userdata
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_user_token_create(self):
        userdata = {
            'email': 'test@test.ru',
            'password': '12345',
        }
        # создаём пользователя
        self.client.post(
            reverse('users:create_user'),
            data=userdata
        )
        response = self.client.post(
            reverse('users:token_obtain_pair'),
            userdata
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_user_token_refresh(self):
        userdata = {
            'email': 'test@test.ru',
            'password': '12345',
        }
        # создаём пользователя
        self.client.post(
            reverse('users:create_user'),
            data=userdata
        )
        tokens = self.client.post(
            reverse('users:token_obtain_pair'),
            userdata
        )
        response = self.client.post(
            reverse('users:token_refresh'),
            {'refresh': tokens.json().get('refresh')}
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )


class HabitTestCase(APITestCase):
    """Тест для контроллера HabitViewSet"""

    def setUp(self):
        """Заполняем БД перед началом тестов"""
        userdata = {
            'email': 'test@test.ru',
            'password': '12345',
        }
        # создаём пользователя
        self.client.post(
            reverse('users:create_user'),
            userdata
        )
        # получаем токен
        response = self.client.post(
            reverse('users:token_obtain_pair'),
            userdata
        )
        # добавляем токен к авторизации
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.json().get('access'))
        # шаблон для создания полезной привычки
        self.habit_data = {
            'title': 'Test habit',
            'place': 'street',
            'time': '10:00:00',
            'action': 'run!',
            'period': '1',
            'reward': 'eat banana!',
            'durations': 60,
            'is_public': False,
            'owner': User.objects.get(email='test@test.ru')
        }

    def test_habit_create(self):
        """Тест создания привычки"""
        data = {
            'title': 'Test habit',
            'place': 'street',
            'time': '10:00:00',
            'action': 'run!',
            'period': '1',
            'reward': 'eat banana!',
            'durations': 60,
            'is_public': 'false'
        }
        response = self.client.post(
            reverse('habits:useful-list'),
            data=data
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_wrong_habit_create(self):
        """Тест валидатора создания и изменения привычки на указание одновременно двух полей reward и nice_habit"""
        nice_data = {
            'title': 'Test habit',
            'place': 'street',
            'time': '10:00:00',
            'action': 'run!',
            'durations': 60,
            'is_public': False,
            'owner': User.objects.get(email='test@test.ru')
        }
        self.nice_habit = NiceHabit.objects.create(**nice_data)
        data = {
            'title': 'Test habit',
            'place': 'street',
            'time': '10:00:00',
            'action': 'run!',
            'period': '1',
            'reward': 'eat banana!',
            'durations': 60,
            'is_public': 'false',
            'nice_habit': self.nice_habit.pk
        }
        response = self.client.post(
            reverse('habits:useful-list'),
            data=data
        )
        self.assertEqual(
            {'non_field_errors': ['Вы можете выбрать только одно из двух: награда или приятная привычка']},
            response.json()
        )

    def test_wrong_period_habit_create(self):
        """Тест валидатора создания и изменения привычки на указание неправильной строки period"""
        wrong_data = {
            'title': 'Test habit',
            'place': 'street',
            'time': '10:00:00',
            'action': 'run!',
            'period': '9qw',
            'durations': 60,
            'is_public': 'false'
        }
        response = self.client.post(
            reverse('habits:useful-list'),
            data=wrong_data
        )
        self.assertEqual(
            {'non_field_errors': ['Вы можете использовать только набор из 7 цифр от 1 до 7']}
            ,
            response.json()
        )

    def test_habit_delete(self):
        """Тест удаления привычки"""
        # сначала добавляем
        self.habit = Habit.objects.create(**self.habit_data)
        # теперь удаляем
        response = self.client.delete(
            reverse('habits:useful-detail', kwargs={'pk': self.habit.pk}),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_habit_detail(self):
        """Тест получения одного объекта модели Habit"""
        # сначала добавляем
        self.habit = Habit.objects.create(**self.habit_data)
        # теперь получаем
        response = self.client.get(
            reverse('habits:useful-detail', kwargs={'pk': self.habit.pk}),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_habit_list(self):
        """Тест получения всех объектов модели Habit"""
        # сначала добавляем
        self.habit = Habit.objects.create(**self.habit_data)
        # теперь получаем
        response = self.client.get(
            reverse('habits:useful-list'),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_habit_update(self):
        """Тест обновления объекта модели Habit"""
        # сначала добавляем
        self.habit = Habit.objects.create(**self.habit_data)
        # теперь обновляем
        data = {
            'title': 'Test2'
        }
        response = self.client.patch(
            reverse('habits:useful-detail', kwargs={'pk': self.habit.pk}),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )


class NiceHabitTestCase(APITestCase):
    """Тест для контроллера HabitViewSet"""

    def setUp(self):
        """Заполняем БД перед началом тестов"""
        userdata = {
            'email': 'test@test.ru',
            'password': '12345',
        }
        # создаём пользователя
        self.client.post(
            reverse('users:create_user'),
            userdata
        )
        # получаем токен
        response = self.client.post(
            reverse('users:token_obtain_pair'),
            userdata
        )
        # добавляем токен к авторизации
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.json().get('access'))
        # шаблон для создания приятной привычки
        self.nice_habit_data = {
            'title': 'Test habit',
            'place': 'street',
            'time': '10:00:00',
            'action': 'run!',
            'durations': 60,
            'is_public': False,
            'owner': User.objects.get(email='test@test.ru')
        }

    def test_nice_habit_create(self):
        """Тест создания приятной привычки"""
        data = {
            'title': 'Test habit',
            'place': 'street',
            'time': '10:00:00',
            'action': 'run!',
            'durations': 60,
            'is_public': 'false'
        }
        response = self.client.post(
            reverse('habits:nice-list'),
            data=data
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_nice_habit_delete(self):
        """Тест удаления приятной привычки"""
        # сначала добавляем
        self.habit = NiceHabit.objects.create(**self.nice_habit_data)
        # теперь удаляем
        response = self.client.delete(
            reverse('habits:nice-detail', kwargs={'pk': self.habit.pk}),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_nice_habit_detail(self):
        """Тест получения одного объекта модели NiceHabit"""
        # сначала добавляем
        self.habit = NiceHabit.objects.create(**self.nice_habit_data)
        # теперь получаем
        response = self.client.get(
            reverse('habits:nice-detail', kwargs={'pk': self.habit.pk}),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_nice_habit_list(self):
        """Тест получения всех объектов модели NiceHabit"""
        # сначала добавляем
        self.habit = NiceHabit.objects.create(**self.nice_habit_data)
        # теперь получаем
        response = self.client.get(
            reverse('habits:nice-list'),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_nice_habit_update(self):
        """Тест обновления объекта модели NiceHabit"""
        # сначала добавляем
        self.habit = NiceHabit.objects.create(**self.nice_habit_data)
        # теперь обновляем
        data = {
            'title': 'Test2'
        }
        response = self.client.patch(
            reverse('habits:nice-detail', kwargs={'pk': self.habit.pk}),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )


class PublicHabitTestCase(APITestCase):
    """Тест для контроллера PublicHabitViewSet"""

    def setUp(self):
        """Заполняем БД перед началом тестов"""
        userdata = {
            'email': 'test@test.ru',
            'password': '12345',
        }
        # создаём пользователя
        self.client.post(
            reverse('users:create_user'),
            userdata
        )
        # получаем токен
        response = self.client.post(
            reverse('users:token_obtain_pair'),
            userdata
        )
        # добавляем токен к авторизации
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.json().get('access'))
        # шаблоны для создания полезной привычки
        self.habit_data_public = {
            'title': 'Test habit',
            'place': 'street',
            'time': '10:00:00',
            'action': 'run!',
            'period': '1',
            'reward': 'eat banana!',
            'durations': 60,
            'is_public': True,
            'owner': User.objects.get(email='test@test.ru')
        }
        self.habit_data_not_public = {
            'title': 'Test habit',
            'place': 'street',
            'time': '10:00:00',
            'action': 'run!',
            'period': '1',
            'reward': 'eat banana!',
            'durations': 60,
            'is_public': False,
            'owner': User.objects.get(email='test@test.ru')
        }

    def test_public_habit_list(self):
        """Тест получения всех публичных объектов модели Habit"""
        # сначала добавляем
        self.habit_public = Habit.objects.create(**self.habit_data_public)
        self.habit_not_public = Habit.objects.create(**self.habit_data_not_public)
        # теперь получаем
        response = self.client.get(
            reverse('habits:public_useful_habit_list'),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )


class PublicNiceHabitTestCase(APITestCase):
    """Тест для контроллера PublicNiceHabitViewSet"""

    def setUp(self):
        """Заполняем БД перед началом тестов"""
        userdata = {
            'email': 'test@test.ru',
            'password': '12345',
        }
        # создаём пользователя
        self.client.post(
            reverse('users:create_user'),
            userdata
        )
        # получаем токен
        response = self.client.post(
            reverse('users:token_obtain_pair'),
            userdata
        )
        # добавляем токен к авторизации
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.json().get('access'))
        # шаблоны для создания полезной привычки
        self.nice_habit_data_public = {
            'title': 'Test habit',
            'place': 'street',
            'time': '10:00:00',
            'action': 'run!',
            'durations': 60,
            'is_public': True,
            'owner': User.objects.get(email='test@test.ru')
        }
        self.nice_habit_data_not_public = {
            'title': 'Test habit',
            'place': 'street',
            'time': '10:00:00',
            'action': 'run!',
            'durations': 60,
            'is_public': False,
            'owner': User.objects.get(email='test@test.ru')
        }

    def test_public_habit_list(self):
        """Тест получения всех публичных объектов модели NiceHabit"""
        # сначала добавляем
        self.nice_habit_public = NiceHabit.objects.create(**self.nice_habit_data_public)
        self.nice_habit_not_public = NiceHabit.objects.create(**self.nice_habit_data_not_public)
        # теперь получаем
        response = self.client.get(
            reverse('habits:public_nice_habit_list'),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
