from django.core.validators import RegexValidator

hiragana_only_validator = RegexValidator(
    regex=r'^[ぁ-ゖー]+$',
    message='ひらがなのみ入力可能です。',
    code='invalid',
)
