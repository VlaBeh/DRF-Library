from django.db import models

from django.db import models
from borrowings.models import Borrowing


class Payment(models.Model):
    PENDING = 'PENDING'
    PAID = 'PAID'
    STATUS_CHOICES = [(PENDING, 'Pending'), (PAID, 'Paid')]

    borrowing = models.OneToOneField(Borrowing, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    session_url = models.URLField()
    money_to_pay = models.DecimalField(max_digits=7, decimal_places=2)
