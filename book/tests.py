from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

from book.models import Book

User = get_user_model()


class BooksAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email="admin@example.com",
            password="adminpass"
        )

        token = AccessToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        self.book = Book.objects.create(
            title="Test Book",
            author="Author Name",
            cover="HARD",
            inventory=10,
            daily_fee=1.99
        )

    def test_list_books(self):
        response = self.client.get('/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book_as_admin(self):
        response = self.client.post('/books/', {
            "title": "New Book",
            "author": "New Author",
            "cover": "SOFT",
            "inventory": 5,
            "daily_fee": 2.99
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
