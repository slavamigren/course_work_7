from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from conf import settings


NULLABLE = {'blank': True, 'null': True}


class NiceHabit(models.Model):
    """
    Обязательные поля:
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
    title = models.CharField(max_length=30, verbose_name='название')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE,
                              verbose_name='пользователь')
    place = models.CharField(max_length=100, **NULLABLE, verbose_name='место')
    time = models.TimeField(**NULLABLE, verbose_name='время')
    action = models.CharField(max_length=100, verbose_name='действие')
    period = models.CharField(
        max_length=7,
        default='1234567',
        verbose_name='периодичность'
    )
    durations = models.SmallIntegerField(default=120,
                                         validators=[MaxValueValidator(120), MinValueValidator(1)],
                                         verbose_name='продолжительность')
    is_public = models.BooleanField(default=False, verbose_name='публичная')

    class Meta:
        verbose_name = 'приятная привычка'
        verbose_name_plural = 'приятные привычки'
        ordering = ('title', )

    def __str__(self):
        return self.title


class Habit(models.Model):
    """
    Обязательные поля:
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
    title = models.CharField(max_length=30, verbose_name='название')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE,
                              verbose_name='пользователь')
    place = models.CharField(max_length=100, **NULLABLE, verbose_name='место')
    time = models.TimeField(**NULLABLE, verbose_name='время')
    action = models.CharField(max_length=100, verbose_name='действие')
    nice_habit = models.ForeignKey(
        NiceHabit,
        **NULLABLE,
        on_delete=models.SET_NULL,
        verbose_name='приятная привычка'
    )
    period = models.CharField(
        max_length=7,
        default='1234567',
        verbose_name='периодичность'
    )
    reward = models.CharField(max_length=100, **NULLABLE, verbose_name='вознаграждение')
    durations = models.SmallIntegerField(
        default=120,
        validators=[MaxValueValidator(120), MinValueValidator(1)],
        verbose_name='продолжительность'
    )
    is_public = models.BooleanField(default=False, verbose_name='публичная')

    class Meta:
        verbose_name = 'полезная привычка'
        verbose_name_plural = 'полезные привычки'
        ordering = ('title', )


    def __str__(self):
        return self.title
