# Django 5.2/6.0・Python 3.11–3.14 API 互換監査レポート

> Issue: #13 ／ 監査日: 2026-05-28 ／ Wave 1 先行作業

## TL;DR

- **コアコード（`utils/`・`fields/normalize_char_field`・`ja/`・`templatetags/`・`apps.py`・`base_app_settings`・`fields/ulid`）は Django 5.2 LTS / 6.0 × Python 3.11–3.14 で動作することを実測で確認**。コード変更不要。
- **`base/models/` 配下は `django_boost` の eager import が原因で Django 5/6 環境で詰む**。これは `django_boost` の構造的問題（その `__init__.py` が `EmailUser` 等の独自モデルを読み込む）であり、コード自体の問題ではない。**#15（django-boost インライン化）の実装根拠を実証**したかたちで、#15 完了後に解消される。
- マトリクス CI（#06）は本監査結果と #15・#16 完了を前提に組めばよい。

## スコープと手法

### 1. 静的監査
- `uvx django-upgrade --target-version 5.2` を `ya_django_toolkit_jp/` および `tests/` 配下の全 34 `*.py` ファイルに適用。
- 削除・非推奨が懸念される API の使用箇所を `grep` で列挙し、Django 6.0 上で個別に import 確認。

### 2. 動的検証（マトリクス）
- `uvx --python <ver> --with "django==<ver>"` で ephemeral 環境を作り、既存テスト（`tests/ja/`、8 件）と全モジュールの import を実行。

## 結果

### 静的監査

| 項目 | 結果 |
|---|---|
| `django-upgrade --target-version 5.2` の差分 | **0 ファイル**。既存コードに pre-5.2 の非推奨パターン無し |
| `apps.py: default_auto_field` | Django 5.2/6.0 で標準サポート（変更なし） |
| `templatetags`: `escape_uri_path`・`reverse`/`NoReverseMatch`・`resolver_match.view_name` | **Django 6.0 で全て import 可能・関数として動作**（UTF-8 含む実呼び出しで確認） |
| `utils/view.py`: `ResolverMatch.app_name` | 安定属性。問題なし |
| `fields/normalize_char_field`・`ja/fields/{hiragana,katakana}_char`: `CharField.to_python` シグネチャ | 旧来どおり `(self, value)`。問題なし |
| `fields/ulid`: `models.UUIDField` 継承 | 問題なし |

### 動的検証（既存テスト 8 件 + 全モジュール import）

| Python | Django | 既存テスト | コア import | `base/models` |
|---|---|---|---|---|
| 3.11 | 5.2 LTS | ✅ 8 OK | ✅ | ⚠️ ※ |
| 3.12 | 6.0 | ✅ 8 OK | ✅ | ⚠️ ※ |
| 3.13 | 6.0 | ✅ 8 OK | ✅ | ⚠️ ※ |
| 3.14 | 5.2 LTS | ✅ 8 OK | ✅ | ⚠️ ※ |
| 3.14 | 6.0 | ✅ 8 OK | ✅ | ⚠️ ※ |

※ `base/models/*` の import 自体は **`django_boost.models.__init__` が `EmailUser` 等の独自モデルを eager に読み込み、`django_boost` を `INSTALLED_APPS` に登録していないと app_label エラーで詰む**。これは Django のバージョンを問わず（5.2 でも 6.0 でも）発生する `django_boost` 側の構造問題で、本リポジトリのコード自体には非推奨/削除 API は使われていない。

`fields/ulid` の動的生成（`default()` 経由の UUID 生成）は **ulid-py が Python 3.14 でも現行コードのまま動作**することを別途確認済み（#16 の調査時に実測）。

## 結論と引き継ぎ

- **本 Issue 範囲のコード修正は不要**。`django-upgrade` も手動監査も「修正なし」で完了。
- **`base/models/` のランタイム検証は #15（`django_boost` インライン撤廃）完了後に再評価**する。#15 完了後は `django_boost` 由来の eager import が消えるため、Django 5.2/6.0 マトリクスで base/models も実用可能になる見込み。
- **#06（nox マトリクス）**は本監査結果 + #15 + #16 完了を前提に、`Django 5.2 / 6.0 × Python 3.11–3.14`（6.0 × 3.11 は exclude）と `[all]` extras の python-ulid / ulid-py 両セッションを組めば green になる見込み。

## 参考

- 検証コマンド例:
  ```bash
  uvx django-upgrade --target-version 5.2 $(find ya_django_toolkit_jp tests -name '*.py')
  uvx --python 3.14 --with "django>=6.0,<6.1" -- python -m unittest discover ./tests/
  ```
- 関連 Issue: #14（uv 移行・PR #26）/ #15（django-boost 撤廃）/ #16（ULID 両対応）/ #06（nox マトリクス）。
