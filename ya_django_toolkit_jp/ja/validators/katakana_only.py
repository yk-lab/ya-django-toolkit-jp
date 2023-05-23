from django.core.validators import RegexValidator

katakana_only_validator = RegexValidator(
    regex=r'^[ァ-ヶー]+$',
    message='カタカナのみ入力可能です。',
    code='invalid',
)
