from rest_framework import serializers

from tracker.models import Habit
from tracker.validators import validate_habit_reward, validate_time_to_complete, validate_related_habit, \
    validate_periodicity, validate_pleasant_habit


class HabitSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели привычки
    """

    class Meta:
        model = Habit
        fields = '__all__'

    def validate(self, attrs):
        related_habit = attrs.get('related_habit')
        award = attrs.get('award')
        time_to_complete = attrs.get('time_to_complete')
        pleasant_habit = attrs.get('pleasant_habit')
        periodicity = attrs.get('periodicity')
        validate_habit_reward(related_habit, award)
        validate_time_to_complete(time_to_complete)
        validate_related_habit(related_habit)
        validate_pleasant_habit(pleasant_habit, related_habit, award)
        validate_periodicity(periodicity)
        return attrs

