from django.core.exceptions import ValidationError


def validate_habit_reward(related_habit, award):
    # Проверка на одновременное заполнение двух полей
    if related_habit and award:
        raise ValidationError(
            "Нельзя одновременно указывать и вознаграждение, и связанную привычку."
        )


def validate_time_to_complete(time_to_complete):
    # Проверка на то, что время выполнения не должно быть более 120 секунд.
    total_second = (time_to_complete.hour * 3600 + time_to_complete.minute * 60 + time_to_complete.second)
    if total_second > 120:
        raise ValidationError(
            "Нельзя чтобы привычка длилась более 2 минут"
        )


def validate_related_habit(related_habit):
    # Проверка на то, что в связанные могут попадать только привычки с признаком приятной.
    if related_habit and not related_habit.pleasant_habit:
        raise ValidationError(
            "В связанные привычки могут попадать только привычки с признаком приятной привычки."
        )


def validate_pleasant_habit(pleasant_habit, related_habit, award):
    # Проверка на то, что у приятной привычки не может быть вознаграждения или связанной привычки.
    if pleasant_habit and (related_habit or award):
        raise ValidationError(
            "У приятной привычки не может быть вознаграждения или связанной привычки."
        )


def validate_periodicity(periodicity):
    # Проверка на то, что привычка выполняется не реже чем раз в неделю.
    if periodicity > 7:
        raise ValidationError(
            "Нельзя выполнять привычку реже, чем 1 раз в 7 дней."
        )
