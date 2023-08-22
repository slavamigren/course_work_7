from rest_framework import serializers

from habits.models import Habit, NiceHabit
from habits.validators import RewardValidator, PeriodValidator


class NiceHabitSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Habit
    """
    class Meta:
        model = NiceHabit
        fields = '__all__'


class HabitSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Habit
    """
    nice_habit_description = NiceHabitSerializer(source='nice_habit', read_only=True)

    class Meta:
        model = Habit
        fields = '__all__'
        validators = [RewardValidator(), PeriodValidator()]


class PublicHabitSerializer(serializers.ModelSerializer):
    """Сериализатор публичных полей модели Habit"""
    class Meta:
        model = Habit
        exclude = ('is_public', 'owner', 'id')


class PublicNiceHabitSerializer(serializers.ModelSerializer):
    """Сериализатор публичных полей модели NiceHabit"""
    class Meta:
        model = NiceHabit
        exclude = ('is_public', 'owner', 'id')
