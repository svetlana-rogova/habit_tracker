from django.db import models


class Habit(models.Model):
    """
    Модель привычки
    """

    owner = models.ForeignKey(
        "user.CustomUser", on_delete=models.CASCADE, related_name="habit", verbose_name="Пользователь"
    )
    place = models.CharField(max_length=100, verbose_name="Место")
    time = models.DateTimeField(verbose_name="Время начала выполнения")
    action = models.TextField(verbose_name="Действие")
    pleasant_habit = models.BooleanField(default=False, verbose_name="Признак приятной привычки")
    related_habit = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Связанная привычка"
    )
    periodicity = models.PositiveIntegerField(default=1, verbose_name="Периодичность")
    award = models.TextField(verbose_name="Вознаграждение", null=True, blank=True)
    time_to_complete = models.TimeField(verbose_name="Время на выполнение")
    is_public = models.BooleanField(default=False, verbose_name="Опубликовать")

    def __str__(self):
        return f"{self.action}"

    class Meta:
        verbose_name = "привычка"
        verbose_name_plural = "привычки"
