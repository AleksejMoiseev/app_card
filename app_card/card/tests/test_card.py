from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User

from card.models import Card, ONE_MONTH


class CardApiTestCase(APITestCase):
    fixtures = ['cards', 'user']

    def setUp(self) -> None:
        self.admin = User.objects.get(username='admin')
        self.user = User.objects.get(username='User')
        self.password_user = '1Qwerty1'
        self.admin_password = '1111'

    def test_get_all_cards_admin(self):
        self.client.login(username='admin', password=self.admin_password)
        response = self.client.get('/admin/card/card/')
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)

    def test_get_all_cards_user(self):
        self.client.login(username='User', password=self.password_user)
        response = self.client.get('/admin/')
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        response = self.client.get('/admin/card/card/generate/')
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)

    def test_positive_create_cards(self):
        self.client.login(username='User', password=self.password_user)
        data = {
            'series': 1002,
            'amount': 2,
            'validity': ONE_MONTH
        }
        response = self.client.post(path='generate', data=data)
