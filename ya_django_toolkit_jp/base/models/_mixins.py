"""抽象モデル用の内部 mixin。

旧来は `django_boost.models.mixins.{TimeStampModelMixin, UUIDModelMixin}` を
利用していたが、django-boost 自体が未保守で Django 5/6 では import 副作用に
よる詰まりが生じるため、必要な mixin だけ自前再実装してインライン化した。

フィールド定義（列名・型・default・editable・verbose_name 含む）は django_boost
版と完全に一致させているため、downstream で `AlterField` 差分は出ない。
"""

from __future__ import annotations

import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampModelMixin(models.Model):
    """`created_at` / `updated_at` フィールドを提供する抽象 mixin。"""

    created_at = models.DateTimeField(
        verbose_name=_('created date'), auto_now_add=True)
    updated_at = models.DateTimeField(
        verbose_name=_('updated date'), auto_now=True)

    class Meta:
        abstract = True


class UUIDModelMixin(models.Model):
    """主キーを UUID（`uuid4`）に置き換える抽象 mixin。"""

    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, unique=True, editable=False)

    class Meta:
        abstract = True
