from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User
from book.models import Book
from borrowings.models import Borrowing
from datetime import date, timedelta


class BorrowingsAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123"
        )
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="adminpass"
        )
        self.book = Book.objects.create(
            title="Borrowed Book",
            author="Author",
            cover="HARD",
            inventory=5,
            daily_fee=2.00
        )
        self.borrowing = Borrowing.objects.create(
            book=self.book,
            user=self.user,
            borrow_date=date.today(),
            expected_return_date=date.today() + timedelta(days=7)
        )

    def test_create_borrowing(self):
        token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post('/borrowings/', {
            "book": self.book.id,
            "expected_return_date": str(date.today() + timedelta(days=7))
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_borrowings(self):
        token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/borrowings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_admin_can_view_all_borrowings(self):
        token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/borrowings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
