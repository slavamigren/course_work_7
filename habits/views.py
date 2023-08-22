from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from habits.models import Habit, NiceHabit
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer, NiceHabitSerializer, PublicHabitSerializer, PublicNiceHabitSerializer


class HabitViewSet(ModelViewSet):
    """Контроллер полезных привычек"""
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        """Показывает только привычки, принадлежащие текущему пользователю"""
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """Добавляет текущего пользователя в качестве владельца созданной привычки"""
        new_habit = serializer.save()
        new_habit.owner = self.request.user
        new_habit.save()


class NiceHabitViewSet(ModelViewSet):
    """Контроллер приятных привычек"""
    queryset = NiceHabit.objects.all()
    serializer_class = NiceHabitSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        """Показывает только привычки, принадлежащие текущему пользователю"""
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """Добавляет текущего пользователя в качестве владельца созданной привычки"""
        new_habit = serializer.save()
        new_habit.owner = self.request.user
        new_habit.save()


class PublicHabitListView(ListAPIView):
    """Контроллер вывода публичных полезных привычек"""
    serializer_class = PublicHabitSerializer
    queryset = Habit.objects.filter(is_public=True)


class PublicNiceHabitListView(ListAPIView):
    """Контроллер вывода публичных приятных привычек"""
    serializer_class = PublicNiceHabitSerializer
    queryset = NiceHabit.objects.filter(is_public=True)
