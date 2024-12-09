from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Уникальні імена для зворотних зв'язків
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',  # Уникальні імена для зворотних зв'язків
        blank=True,
    )
