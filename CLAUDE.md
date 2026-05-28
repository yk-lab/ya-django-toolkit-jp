# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

`ya-django-toolkit-jp` は、日本語（マルチバイト文字）を考慮した Django プロジェクト向けユーティリティを提供する**ライブラリ**（PyPI パッケージ）です。実行アプリケーションではなく、他の Django プロジェクトに `import` して使われる再利用部品の集合です。

- Python 3.11 / Django 4.2 系
- 依存管理は **Poetry**
- テストは **標準ライブラリの `unittest`**（pytest ではない）

## 開発コマンド

```bash
# セットアップ（コア + 開発依存）
poetry install --no-root --with dev
poetry run pre-commit install

# 全テスト（coverage 計測込み。taskipy 経由）
poetry run task test

# 単一テストの実行（unittest のドット記法）
poetry run python -m unittest tests.ja.test_utils.TestUtilsMethods.test_normalize

# Lint / フォーマット（pre-commit 経由で flake8・isort・autopep8 等が走る）
poetry run pre-commit run --all-files

# CHANGELOG 生成（gh2changelog を使用）
poetry run task generate_changelog
```

`poetry run task test` の実体は `coverage run --source ./ya_django_toolkit_jp/ -m unittest discover ./tests/` です。

### オプション依存に依存する機能をテストするとき

`ulid-py` と `django-boost` は **オプション依存**（`all` グループ）で、`--with dev` だけのインストールには含まれません。`ULIDField` / `base/models/` 配下を触る場合は併せて入れてください。

```bash
poetry install --no-root --with dev,all
```

## アーキテクチャ

パッケージ本体は `ya_django_toolkit_jp/` 配下。役割ごとに以下へ分かれます。

- `utils/` — Django 非依存寄りの汎用関数群。`file.py`（Content-Disposition 生成、非 ASCII ファイル名は RFC 5987 形式へ）、`ip.py` / `ipv6.py`（IPv4/IPv6 ⇔ 整数変換、CIDR 範囲算出）、`mimetypes.py`、`view.py`（`app_name:view_name` 形式の名前解決）。
- `fields/` — 汎用モデルフィールド。`NormalizeCharField`（`to_python` で NFKC 正規化）、`ULIDField`（`UUIDField` を基盤に ULID をデフォルト生成）。
- `base/models/` — `django_boost` の Mixin を組み合わせた抽象ベースモデル（`BaseModel` / `BaseUUIDModel` / `BaseULIDModel` / `ULIDModel`）。すべて `abstract = True`。
- `ja/` — 日本語特化機能。`utils.py`（制御文字除去・NFKC 正規化・ひらがな⇔カタカナ変換・各種ハイフンの半角統一）、`fields/`（`HiraganaCharField` / `KatakanaCharField`：`to_python` で自動変換しつつ `default_validators` を付与）、`validators/`（`hiragana_only_validator` / `katakana_only_validator`：`RegexValidator`、エラーメッセージは日本語）。
- `templatetags/ya_django_toolkit_jp.py` — テンプレートタグ `is_active_view`（複数 view 名・list/tuple 受け付け）、`is_active_link`。
- `base_app_settings.py` — prefix 付き Django settings へアクセスするための `BaseAppSettings` パターン（モジュール自体を設定インスタンスに差し替える使い方を docstring に記載）。

### 押さえておくべき設計上の約束

- **オプション依存はガードする**: `ulid-py` / `django-boost` 未インストールでもコア（Django のみ）が動くこと。`fields/ulid.py` は import を `try/except ImportError` で囲み、未導入時は使用時に `ImportError` を送出する。新規に重い依存を足すときは同じ方針を取る。
- **公開 API は `__init__.py` で再エクスポート**: 各サブパッケージの `__init__.py` が `from .x import Y  # noqa: F401` で公開する。新しいフィールド/バリデータを追加したら対応する `__init__.py` にも追記する。
- **日本語フィールドの責務**: `Hiragana/KatakanaCharField` は「`to_python` で表記ゆれを吸収（正規化＋かな種別変換）」と「`default_validators` で入力種別を制約」の二段構え。正規化ロジックは `ja/utils.py` に集約し、フィールド側では再実装しない。

## コーディング規約（pre-commit で強制）

- **文字列はシングルクォート**: `double-quote-string-fixer` フックが `"..."` を `'...'` に書き換える。新規コードは最初からシングルクォートで書く。
- 型ヒントを使うファイルは先頭に `from __future__ import annotations` を置く（`str | None` 記法のため）。
- Lint は flake8 + flake8-isort、整形は autopep8。`migrations/` は除外対象。
- `main` / `develop` への直接コミットは `no-commit-to-branch` フックでブロックされる。作業はブランチを切って行う。
- codespell によるスペルチェックがあるため、英文コメント・識別子のタイポに注意。

## リリースとバージョニング

- バージョンは **git タグから自動決定**（`poetry-git-version-plugin`）。`pyproject.toml` の `version = "0.0.0"` はプレースホルダで、手動更新しない。
- `vX.Y.Z` タグの push → ドラフトリリース作成（`create_draft_release.yml`）→ リリース公開で PyPI へ publish（`pypi_publish.yml`、Trusted Publishing）。
- CI（`python.yml`）は PR 時に safety チェック・`poetry check`・変更ファイルへの pre-commit・`task test` を実行する。
