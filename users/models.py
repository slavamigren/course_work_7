from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='email')
    is_active = models.BooleanField(default=True, verbose_name='user active')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
