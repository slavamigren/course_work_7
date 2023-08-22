from rest_framework.serializers import ValidationError


class RewardValidator:
    """Валидатор проверяет, что выбрано только одно из двух: награда или приятная привычка"""

    def __call__(self, value):
        if value.get('reward', None) and value.get('nice_habit', None):
            raise ValidationError('Вы можете выбрать только одно из двух: награда или приятная привычка')


class PeriodValidator:
    """Валидатор проверяет, что выбрано только одно из двух: награда или приятная привычка"""

    def __call__(self, value):
        period = value.get('period', None)
        period_set = set(str(period))
        if period and (period_set - {'1', '2', '3', '4', '5', '6', '7'}):
            raise ValidationError('Вы можете использовать только набор из 7 цифр от 1 до 7')