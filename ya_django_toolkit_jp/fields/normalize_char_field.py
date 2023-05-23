from __future__ import annotations

from typing import Any

from django.db.models.fields import CharField

from ..ja.utils import normalize


class NormalizeCharField(CharField):
    def to_python(self, value: Any) -> str | None:
        val: str | None = super().to_python(value)
        if isinstance(val, str):
            val = normalize(val)
        return val
