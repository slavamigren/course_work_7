from datetime import datetime
from time import sleep
import requests

from conf.settings import TELEGRAM_TOKEN
from habits.models import Habit, NiceHabit


def send_telegram_message(telegram_id, message):
    """Отправляет сообщение message пользователю телеграмм с id telegram_id"""
    params = {
        'chat_id': telegram_id,
        'text': message
    }
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    requests.get(url, params)

def run_habits():
    """
    Просматривает все полезные и приятные привычки, выбирает соответствующие текущей дате
    и времени и рассылает их владельцам
    """
    current_time = datetime.now().time().replace(second=0, microsecond=0)
    current_week_day = str(datetime.now().isoweekday())

    # выбираем полезные привычки с рассылкой сегодня в текущее время
    useful_habits = Habit.objects.filter(time=current_time, period__contains=current_week_day)

    # выбираем приятные привычки, привязанные к полезным привычкам с рассылкой сегодня в текущее время
    nice_habits = NiceHabit.objects.filter(
        id__in=Habit.objects.filter(nice_habit__isnull=False).values_list('nice_habit_id', flat=True),
        time=current_time,
        period__contains=current_week_day
    )

    if useful_habits:
        for habit in useful_habits:
            reward = ''
            if habit.reward:
                reward = f'Ваша награда: {habit.reward}'
            message = f'Выполните:{habit.action} {habit.place}, у вас есть {habit.durations} секунд.{reward}'
            send_telegram_message(habit.owner.telegram, message)
            sleep(2)  # задержка, чтобы телеграмм не забанил за рассылку спама

    if nice_habits:
        for habit in nice_habits:
            message = f'Насладитесь:{habit.action} {habit.place}, у вас есть {habit.durations} секунд.'
            send_telegram_message(habit.owner.telegram, message)
            sleep(2)  # задержка, чтобы телеграмм не забанил за рассылку спама
