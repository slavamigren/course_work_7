from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from habits.models import Habit, NiceHabit
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer, NiceHabitSerializer, PublicHabitSerializer, PublicNiceHabitSerializer


class HabitViewSet(ModelViewSet):
    """
    Контроллер полезных привычек
    Обязательные поля модели Habit:
        title: CharField, max_length=30, название привычки
        action: CharField, max_length=100, короткое описание действия
        period: CharField, max_length=7, default='1234567' периодичность действия (и напоминания о действии)
        строка с номерами дней недели, могут использоваться только цифры от 1 до 7
        durations: SmallIntegerField, default=120, min=1, max=120, продолжительность действия
        в секундах, максимум 120 секунд

    Необязательные поля:
        place: CharField, max_length=100, место для действия
        time: TimeField, время для действия, секунды должны быть 00
        nice_habit: ForeignKey(NiceHabit) приятная привычка, привязанная к этой полезной привычке,
        может быть заполнено одно из двух полей nice_habit или reward
        reward: CharField, max_length=100, вознаграждение за выполненное действие, может быть заполнено
        одно из двух полей reward или nice_habit
        is_public: BooleanField, default=False, признак публичности привычки, если True, привычку могут
        просматривать все пользователи ресурса
    """
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
    """
    Контроллер приятных привычек
    Обязательные поля модели NiceHabit:
        title: CharField, max_length=30, название привычки
        action: CharField, max_length=100, короткое описание действия
        durations: SmallIntegerField, default=120, min=1, max=120, продолжительность действия
        в секундах, максимум 120 секунд

    Необязательные поля:
        place: CharField, max_length=100, место для действия
        time: TimeField, время для действия, секунды должны быть 00
        is_public: BooleanField, default=False, признак публичности привычки, если True, привычку могут
        просматривать все пользователи ресурса
    """
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
