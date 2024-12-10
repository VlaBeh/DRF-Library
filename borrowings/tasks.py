from django.utils.timezone import now
from notifications.utils import send_telegram_message
from borrowings.models import Borrowing
from celery import shared_task


@shared_task
def check_overdue_borrowings_task():
    check_overdue_borrowings()


def check_overdue_borrowings():
    overdue_borrowings = Borrowing.objects.filter(
        actual_return_date__isnull=True,
        expected_return_date__lt=now().date()
    )
    if not overdue_borrowings.exists():
        send_telegram_message("No borrowings overdue today!")
    else:
        for borrowing in overdue_borrowings:
            message = (
                f"Overdue Borrowing Alert:\n"
                f"User: {borrowing.user.email}\n"
                f"Book: {borrowing.book.title}\n"
                f"Expected Return: {borrowing.expected_return_date}"
            )
            send_telegram_message(message)
