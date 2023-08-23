from celery import shared_task

from habits.services import run_habits


@shared_task
def check_habits_and_send():
    """
    Таск, проверяющий время и день отправки привычки и отправляющий сообщение в телеграмм.
    Необходимо добавить этот таск в Periodic Tasks на исполнение каждую минуту
    """
    run_habits()
