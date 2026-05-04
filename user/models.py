from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Модель пользователя
    """
    chat_id = models.IntegerField(unique=True)


    def __str__(self):
        return self.chat_id