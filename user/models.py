from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Модель пользователя
    """
    email = models.EmailField(unique=True, verbose_name='Email')
    username = models.CharField(max_length=50, blank=True, null=True, verbose_name='Ник')
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name='Номер телефона')
    chat_id = models.CharField(max_length=50, blank=True, null=True, verbose_name='id чата в Telegram')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
