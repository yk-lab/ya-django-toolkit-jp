from __future__ import annotations

from django.db.models.fields import CharField

from ..utils import hiragana_to_katakana
from ..validators import katakana_only_validator


class KatakanaCharField(CharField):
    default_validators = [katakana_only_validator]

    def to_python(self, value):
        value = super().to_python(value)
        return hiragana_to_katakana(value) if value else value
