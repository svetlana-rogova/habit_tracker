from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from user.models import CustomUser
from tracker.models import Habit
from django.urls import reverse
from datetime import time


class HabitTestCase(APITestCase):

    def setUp(self) -> None:

        self.client = APIClient()

        self.user = CustomUser.objects.create_user(username='test', email='user@test.com', password='1234', chat_id='1234' )

        self.other_user = CustomUser.objects.create_user(username='owner',email='user2@test2.com', password='14', chat_id='14' )

        self.pleasant_habit = Habit.objects.create(
            owner=self.other_user,
            place="Дом",
            time="2026-05-11T18:00:00Z",
            action="Отдых",
            pleasant_habit=True,
            periodicity=1,
            time_to_complete="00:01:00",
            is_public=True,
        )

        self.normal_habit = Habit.objects.create(
            owner=self.user,
            place="Дом",
            time="2026-05-11T18:00:00Z",
            action="Учиться",
            pleasant_habit=False,
            periodicity=1,
            time_to_complete="00:01:00",
            is_public=True,
        )


    def test_habit_create_bad(self):
        """
        Проверка на ошибку при создании приятой привычки с вознаграждением
        """
        self.client.force_authenticate(user=self.user)
        test_data = {
            "place": "Дом",
            "time": "2026-05-11T18:00:00",
            "action": "Читать книгу",
            "pleasant_habit": True,
            "periodicity": 1,
            "award": "Шоколадка",
            "time_to_complete": "00:00:30",
            "is_public": False,
        }
        response = self.client.post(reverse('tracker:habit-list'), test_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['non_field_errors'][0],'У приятной привычки не может быть вознаграждения или '
                                                              'связанной привычки.')

    def test_habit_create_bad_time(self):
        """
        Проверка на длительность выполнения привычки
        """
        self.client.force_authenticate(user=self.user)
        test_data = {
            "place": "Дом",
            "time": "2026-05-11T18:00:00",
            "action": "Читать книгу",
            "pleasant_habit": False,
            "periodicity": 1,
            "award": "Шоколадка",
            "time_to_complete": "00:30:00",
            "is_public": True,
        }
        response = self.client.post(reverse('tracker:habit-list'), test_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['non_field_errors'][0],'Нельзя чтобы привычка длилась более 2 минут')

    def test_habit_create_bad_periodic(self):
        """
        Проверка на выполнение привычки не менее 1 раза в неделю
        """
        self.client.force_authenticate(user=self.user)
        test_data = {
            "place": "Дом",
            "time": "2026-05-11T18:00:00",
            "action": "Читать книгу",
            "pleasant_habit": False,
            "periodicity": 10,
            "award": "Шоколадка",
            "time_to_complete": "00:00:30",
            "is_public": True,
        }
        response = self.client.post(reverse('tracker:habit-list'), test_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['non_field_errors'][0],'Нельзя выполнять привычку реже, '
                                                              'чем 1 раз в 7 дней.')

    def test_related_must_be_pleasant(self):
        """
        В связанные привычки должны попадать только приятные привычки
        """
        self.client.force_authenticate(user=self.user)
        test_data = {
            "place": "Дом",
            "time": "2026-05-11T18:00:00",
            "action": "Читать книгу",
            "pleasant_habit": False,
            "periodicity": 1,
            "related_habit": self.normal_habit.id,
            "time_to_complete": "00:00:30",
            "is_public": True,
        }
        response = self.client.post(reverse('tracker:habit-list'), test_data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['non_field_errors'][0],'В связанные привычки могут попадать только '
                                                              'привычки с признаком приятной привычки.')

    def test_award_and_related_forbidden(self):
        """
         Проверка на одновременное использование вознаграждения и полезной привычки
        """
        self.client.force_authenticate(user=self.user)

        test_data = {
            "place": "Дом",
            "time": "2026-05-11T18:00:00",
            "action": "Читать книгу",
            "pleasant_habit": False,
            "periodicity": 1,
            "award": "Шоколадка",
            "related_habit": self.pleasant_habit.id,
            "time_to_complete": "00:00:30",
            "is_public": True,
        }

        response = self.client.post(reverse('tracker:habit-list'), test_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.data['non_field_errors'][0]),'Нельзя одновременно указывать и '
                                                                   'вознаграждение, и связанную привычку.')

    def test_public_list(self):
        """
        Показывает список публичных привычек
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('tracker:habit-public'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)

    def test_detail_owner(self):
        """
        Проверка на вывод привычки для владельца
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('tracker:habit-detail', args=[self.normal_habit.id]))
        self.assertEqual(response.status_code, 200)

    def test_detail_not_owner(self):
        """
        Проверка на вывод привычки для пользователя (не владелец)
        """
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(reverse('tracker:habit-detail', args=[self.normal_habit.id]))
        self.assertEqual(response.status_code, 404)

    def test_put_owner(self):
        """
        Проверка на обновление привычки для владельца
        """
        self.client.force_authenticate(user=self.user)
        data = {
            "place": "Дом",
            "time": "2026-05-11T18:00:00Z",
            "action": "Новая привычка",
            "pleasant_habit": False,
            "periodicity": 1,
            "time_to_complete": "00:01:00",
            "is_public": True,
        }
        response = self.client.put(reverse('tracker:habit-detail', args=[self.normal_habit.id]), data)
        self.assertEqual(response.status_code, 200)

    def test_put_not_owner(self):
        """
        Проверка на обновление привычки для пользователя, который не является владельцем
        """
        self.client.force_authenticate(user=self.other_user)
        data = {
            "place": "Дом",
            "time": "2026-05-11T18:00:00Z",
            "action": "Новая привычка",
            "pleasant_habit": False,
            "periodicity": 1,
            "time_to_complete": "00:01:00",
            "is_public": True,
        }
        response = self.client.put(reverse('tracker:habit-detail', args=[self.normal_habit.id]), data)
        self.assertEqual(response.status_code, 404)

    def test_destroy_owner(self):
        """
        Проверка на удаление привычки для владельца
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('tracker:habit-detail', args=[self.normal_habit.id]))
        self.assertEqual(response.status_code, 204)

    def test_destroy_not_owner(self):
        """
        Проверка на удаление привычки для пользователя, который не является владельцем
        """
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(reverse('tracker:habit-detail', args=[self.normal_habit.id]))
        self.assertEqual(response.status_code, 404)
