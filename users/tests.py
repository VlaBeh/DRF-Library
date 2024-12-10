from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User


class UsersAPITestCase(APITestCase):
    def test_register_user(self):
        response = self.client.post('/users/', {
            "username": "test",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "securepassword"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'], 'test@example.com')

    def test_login_user(self):
        user = User.objects.create_user(
            username="test",
            email="test@example.com",
            password="securepassword"
        )

        response = self.client.post('/users/token/', {
            "email": "test@example.com",
            "password": "securepassword"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_access_protected_route(self):
        user = User.objects.create_user(
            username="test",
            email="test@example.com",
            password="securepassword"
        )

        response = self.client.post('/users/token/', {
            "email": "test@example.com",
            "password": "securepassword"
        })
        access_token = response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        protected_response = self.client.get('/protected-endpoint/')
        self.assertEqual(protected_response.status_code, status.HTTP_200_OK)
