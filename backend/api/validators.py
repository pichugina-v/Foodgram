from django.core.exceptions import ValidationError

COOKING_TIME_AMOUNT_VALIDATION = ('Убедитесь, что это значение '
                                  'больше либо равно 1')


def validate_cooking_time(value):
    if value <= 0:
        raise ValidationError(
            COOKING_TIME_AMOUNT_VALIDATION
        )


def validate_amount(value):
    if value <= 0:
        raise ValidationError(
            COOKING_TIME_AMOUNT_VALIDATION
        )
