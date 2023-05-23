from __future__ import annotations

from django.db.models.fields import CharField

from ..utils import katakana_to_hiragana
from ..validators import hiragana_only_validator


class HiraganaCharField(CharField):
    default_validators = [hiragana_only_validator]

    def to_python(self, value):
        value = super().to_python(value)
        return katakana_to_hiragana(value) if value else value
