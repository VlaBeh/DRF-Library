from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from notifications.utils import send_telegram_message
from .models import Borrowing
from .serializers import BorrowingSerializer


class BorrowingViewSet(ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return super().get_queryset()
        return Borrowing.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        borrowing = serializer.save(user=self.request.user)
        send_telegram_message(f"New borrowing created: {borrowing.book.title}")
