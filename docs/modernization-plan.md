# ya-django-toolkit-jp 近代化プラン

> 3年ぶり（最終リリース v0.0.3 / 2023-05-31）の保守再開に向けた調査結果と決定事項の記録。
> 調査日: 2026-05-27

## 決定事項サマリ

| 項目 | 決定 | 補足 |
|---|---|---|
| パッケージ管理 | **uv へ移行** | PEP 621 化 + dynamic versioning + タスクランナー差し替えが伴う |
| Lint / Format | **ruff に統合 + ダブルクォートへ統一** | flake8 / isort / autopep8 / double-quote-string-fixer を撤去 |
| テスト | **pytest + pytest-django へ移行し、未テスト領域も拡充** | 既存 unittest はそのまま動く |
| サポート範囲 | **Django 5.2 LTS + 6.0 × Python 3.11–3.14** | Django 4.2 は 2026-04 EOL のため対象外 |
| ULID / 時刻順 ID | **ULID バックエンド両対応（python-ulid 推奨 / ulid-py 後方互換）+ `UUIDv7Field` 追加** | ulid-py は 3.14 でも動作するが未保守 |
| django-boost | **2 つの mixin をインライン化し依存撤廃** | MIT 同士・定型コードのため再実装で対応（後述） |
| 言語非依存版 | **単一パッケージ継続 + `normalize` の所属整理** | 将来の分離余地は残す |
| system check | **`ULIDField` を `check()` 方式へ作り替え** | `__init__` 即死をやめる |
| 進め方 | **優先度順に GitHub Issue 化** | 下記「Issue 分割案」参照 |
| タスクランナー | **poethepoet（日常コマンド）+ nox（バージョンマトリクス）** | 追加バイナリ無し・uv 一発で揃う。下記参照 |

## サポート対象バージョン

現行サポートされている Django は実質 5.2 LTS と 6.0 のみ（2026-05 時点）。

| Django | 状態 | 対応 Python |
|---|---|---|
| 4.2 LTS | EOL 2026-04-07（終了済） | 3.8–3.12 |
| 5.0 / 5.1 | EOL 済 | — |
| 5.2 LTS | サポート中（〜2028-04） | 3.10–3.14 |
| 6.0 | 現行（最新 6.0.5） | 3.12–3.14（3.10/3.11 を drop） |

CI マトリクス（`exclude` 必須。6.0 は Python 3.11 非対応）:

| | Django 5.2 | Django 6.0 |
|---|---|---|
| Python 3.11 | ✓ | ✗ |
| Python 3.12 | ✓ | ✓ |
| Python 3.13 | ✓ | ✓ |
| Python 3.14 | ✓ | ✓ |

Python EOL: 3.9=終了 / 3.10=2026-10 / 3.11=2027-10 / 3.12=2028-10 / 3.13=2029-10 / 3.14=2025-10 リリース。

## 論点ごとの詳細

### 1. Poetry → uv
- `uv build` / `uv publish` でビルド・公開・Trusted Publishing まで完結。Poetry 必須の理由はもうない。
- 移行で必要な対応:
  1. `pyproject.toml` の PEP 621 化（`[tool.poetry]` → `[project]`、dev → `[dependency-groups]`、`all` → `[project.optional-dependencies]`）。
  2. git タグ自動バージョニング: `poetry-git-version-plugin` → `uv-dynamic-versioning`（hatchling）または `hatch-vcs`。CI は `fetch-depth: 0` が必須。
  3. タスクランナー: `taskipy` → poethepoet（日常コマンド）。バージョンマトリクスは nox に分担（下記）。

### 2. ruff 統合 + ダブルクォート
- ruff のデフォルトはダブルクォート（Black 互換）。`double-quote-string-fixer` は撤去。
- 反転時に一度だけ全体差分が出るため、**フォーマット変更は独立した PR/コミットに切る**こと（他の変更と混ざると差分が読めなくなる）。

### 3. pytest 移行
- pytest は `unittest.TestCase` をそのまま実行できるため、既存テストは無改変で動く。
- モデル/フィールドのテスト用に pytest-django + 最小テスト設定（`settings.configure()` または `conftest.py`）。
- 現状テストは `ja/utils` と `ja/validators` のみ。**未テスト: `utils/ip`・`file`・`mimetypes`・`view`・`fields/`・`base/models`・`templatetags`** を拡充。

### 4. ULID / UUIDv7
- `ulid-py` は最終リリース 2020-09・未保守だが、**実測で Python 3.12/3.13/3.14 でも現行コードのまま動作する**（壊れていない）。
- 保守されている `python-ulid`（3.1.0 / 2025-08・活発）を新規の推奨にしつつ、**実行時判別で ulid-py / python-ulid の両対応**にする（既存 ulid-py ユーザーは無変更）。判別は `hasattr(ulid, 'api')`、`ULID().to_uuid()` は `uuid.UUID` を返す。
- Python 3.14 で `uuid.uuid6/7/8()` が標準入り（RFC 9562）。`UUIDv7Field` を新設し、3.14+ は `uuid.uuid7()`、それ未満は backport（`uuid-utils` 等）でフォールバック。
- 下限が Python 3.11/3.12 の間は uuid7 標準 API に寄せきれないため、当面は「python-ulid + UUIDv7Field」併存。

### 5. django-boost 撤廃
- django-boost は Django 3.0–4.1・Python 3.8–3.10 までの対応表明（最終リリース 2022-09）。Django 5/6 では未検証。
- 使用しているのは `TimeStampModelMixin`（`created_at`/`updated_at`）と `UUIDModelMixin`（`uuid4` の PK）の 2 つだけ。いずれも数行の定型コード。
- **対応: 自前で再実装してインライン化し、依存を撤廃する。**

#### ライセンスについて（確認済み）
- django-boost は MIT、本プロジェクトも MIT で互換。衝突なし。
- 対象は Django の定型 field 宣言で創作性が低く、「実質的部分のコピー」に当たりにくい。
- 安全策として **コピペではなく独自に再実装**する（それなら表記不要）。万一そのまま転記する場合のみ、MIT の著作権表示・許諾文を `NOTICE` 等に保持すれば足りる。

### 6. system check 対応
- Django 標準の `ImageField`（Pillow 未導入時に `fields.E210`）と同じ手法。
- `ULIDField.check()` をオーバーライドし、依存未インストール時に `checks.Error`（`obj=self`）を返す。`manage.py check` / `runserver` / `migrate` 起動時に、どのモデルのどのフィールドかまで特定して通知。
- 前提: 現状の `__init__` での `ImportError` 即時送出をやめ、「`__init__` は構築を許す → `check()` で通知 → `default()` で実行時の最終防壁」の 3 層へ整理。

### 7. 言語非依存版の分離
- コードは既に約 8 割が言語非依存（`utils/`・`fields/`・`base/models/`・`templatetags/`・`base_app_settings`）。日本語特化は `ja/` 配下のみ。
- 唯一の結合: `fields/normalize_char_field.py` が `ja.utils.normalize` を import。NFKC 正規化＋制御文字除去は Unicode 一般処理なので、**`normalize` を core 側 utils へ移す**（将来の分離への布石）。
- 当面は単一パッケージ継続。需要が見えたら 1 リポジトリから 2 ディストリビューション（core + jp）公開を検討。

### タスクランナー（決定: poethepoet + nox）
2 段構成にする。いずれも Python 製の dev 依存で、外部バイナリを増やさず `uv sync` 一発で揃う。

- **poethepoet（日常コマンド）**: `pyproject.toml` の `[tool.poe.tasks]` に集約。lint / format / test / changelog など日々のコマンドを担当。venv 内で自動実行。`uv run poe <task>`。
- **nox（バージョンマトリクス）**: `noxfile.py`（純 Python）で Django 5.2/6.0 × Python 3.11–3.14 の組み合わせテストを生成。CI のマトリクスと対応。テスト以外のセッション（lint 等）も書けるが、日常コマンドは poethepoet に寄せて役割を分ける。
- 補足: uv 自身のタスクランナー（`[tool.uv.cli]` 等）は議論・実験段階で GA ではないため当面採用しない。将来 uv に吸収された際は poethepoet からの移行コストは小さい。

## その他の更新候補（3 年分の棚卸し）
- GitHub Actions: `checkout@v3`→v5、`setup-python@v4`→v5、`action-gh-release@v1`→v2、uv 化なら `astral-sh/setup-uv` 追加。
- セキュリティ: `safety check --stdin` は非推奨 → **`pip-audit`（`uvx pip-audit`）** へ置換。
- pre-commit の rev が全体的に古い（`pre-commit-hooks v4.3.0`→v6 系ほか）。
- 開発依存の旧版: `mypy 1.3.0`、`django-types 0.17`、`types-backports`（不要の可能性）。型チェックは `django-stubs` 系の現行構成を再検討。
- `.python-version` が `3.11.3` 固定 → 更新。
- README の `poetry install --no-root` はフィールド/モデルテストに不都合な場面あり → 見直し。

## Issue 分割案（優先度順）

> P1 = 破壊的変更が小さく効果大 / P2 = 基盤刷新 / P3 = 追加機能・整理

1. **[P1] 依存健全化** — django-boost インライン撤廃 + ULID バックエンド両対応（python-ulid 推奨 / ulid-py 後方互換）+ `ULIDField` を `check()` 方式へ作り替え。（内部変更中心で互換維持しやすい）
2. **[P1] CI マトリクス整備** — nox で Django 5.2/6.0 × Python 3.11–3.14、4.2 EOL 対応、`.python-version` 更新。
3. **[P2] ツールチェーン移行（uv）** — pyproject PEP 621 化、dynamic versioning、`taskipy`→poethepoet、GitHub Actions 版上げ、`safety`→`pip-audit`。
4. **[P2] Lint/Format（ruff 統合）** — ダブルクォート統一、pre-commit rev 更新。※フォーマット反映は単独 PR。
5. **[P2] テスト（pytest 移行）** — pytest + pytest-django、未テスト領域のカバレッジ拡充。
6. **[P3] `UUIDv7Field` 追加** — 3.14+ stdlib / それ未満は backport。
7. **[P3] `normalize` の所属整理** — `ja.utils` → core utils（言語非依存分離への布石）。
8. **[P3] ドキュメント整備** — README（`--no-root` 見直し等）、CHANGELOG 運用。

## 参考リンク
- Django EOL: https://endoflife.date/django
- Django 6.0 release notes: https://docs.djangoproject.com/en/6.0/releases/6.0/
- uv（build/publish）: https://docs.astral.sh/uv/guides/package/ / uv-dynamic-versioning: https://pypi.org/project/uv-dynamic-versioning/
- Ruff formatter: https://docs.astral.sh/ruff/formatter/
- safety 2.x→3.x 移行: https://docs.safetycli.com/safety-docs/safety-cli/introduction-to-safety-cli-vulnerability-scanning/migrating-from-safety-cli-2.x-to-safety-cli-3.x
- python-ulid: https://pypi.org/project/python-ulid/
- Python uuid（RFC 9562 / uuid7）: https://docs.python.org/3/library/uuid.html
- django-boost: https://github.com/ChanTsune/django-boost （MIT / 対応 Django 3.0–4.1）
