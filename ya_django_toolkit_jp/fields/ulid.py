from django.core import checks
from django.db import models

# ULID バックエンドは python-ulid（保守版・推奨）と ulid-py（後方互換）の両対応。
# 両者は同じ `ulid` モジュール名を占有するため一環境に同居不可。実行時判別する。
try:
    import ulid as _ulid
except ImportError:
    _ulid = None


def default():
    """ULID をベースに `uuid.UUID` を生成する（`UUIDField` 互換）。

    インストールされているバックエンドを実行時判別:
      - ulid-py: `ulid.api` 属性を持つ → `api.Api(providers.DEFAULT).new().uuid`
      - python-ulid: それ以外 → `ulid.ULID().to_uuid()`

    両バックエンド未インストール時は `ImportError`（最終防壁）。通常はモデル定義時に
    `ULIDField.check()` が `ya_django_toolkit_jp.E001` として通知する。
    """
    if _ulid is None:
        raise ImportError(
            'ULIDField requires the `python-ulid` package (recommended) '
            'or `ulid-py` (legacy). '
            'Install with: pip install ya-django-toolkit-jp[all]'
        )
    if hasattr(_ulid, 'api'):
        # ulid-py 後方互換パス
        from ulid import providers
        from ulid.api import api

        return api.Api(providers.DEFAULT).new().uuid
    # python-ulid（推奨）
    return _ulid.ULID().to_uuid()


class ULIDField(models.UUIDField):
    """ULID をベースに UUID として保存するフィールド。

    モデルへの追加・import 時点では ulid バックエンド未インストールでもフィールドは
    構築できる（Django 標準の `ImageField` が Pillow 未導入時に `check()` で通知する
    のと同じ方式）。`manage.py check` が `ya_django_toolkit_jp.E001` で通知し、
    実際に値生成しようとすると `default()` が分かりやすい `ImportError` を出す。
    """

    def __init__(self, primary_key=True, editable=False, *args, **kwargs):
        kwargs.setdefault('primary_key', primary_key)
        kwargs.setdefault('editable', editable)
        kwargs.setdefault('default', default)
        super().__init__(*args, **kwargs)

    def check(self, **kwargs):
        return [*super().check(**kwargs), *self._check_ulid_backend()]

    def _check_ulid_backend(self):
        if _ulid is None:
            return [
                checks.Error(
                    'ULIDField を使うには ulid バックエンドが必要です'
                    '（python-ulid 推奨 / ulid-py も可）。',
                    hint='pip install ya-django-toolkit-jp[all]  '
                    '（または: pip install python-ulid）でインストールしてください。',
                    obj=self,
                    id='ya_django_toolkit_jp.E001',
                )
            ]
        return []
