from __future__ import annotations

import re
import string
import unicodedata

similarly_chars = '0Oo1Il2Zz6b9gCcKkPpSsUuVvWwXxYy'

no_similar_chars = ''.join(
    c for c in string.ascii_letters + string.digits
    if c not in similarly_chars)


def remove_control_characters(s: str) -> str:
    """制御文字を削除する

    Args:
        s (str): 除去対象の文字列

    Returns:
        str: 制御文字を除去した文字列
    """
    return ''.join(ch for ch in s if unicodedata.category(ch)[0] != 'C')


def unicode_normalize(s: str) -> str:
    """Unicode正規化を行う

    Args:
        s (str): 正規化対象の文字列

    Returns:
        str: 正規化した文字列
    """
    return unicodedata.normalize('NFKC', s)


def normalize(s: str) -> str:
    """文字列の正規化を行う

    Notes:
        制御文字を除去し、Unicode正規化を行う

    Args:
        s (str): 正規化対象の文字列

    Returns:
        str: 正規化した文字列
    """
    return unicode_normalize(remove_control_characters(s))


def replace_hyphen(text: str, replace_hyphen: str = '-') -> str:
    """全ての横棒を半角ハイフンに置換する
    Args:
        text (str): 入力するテキスト
        replace_hyphen (str): ハイフンの置換先文字列
    Returns:
        (str): 置換後のテキスト
    """
    # https://qiita.com/non-caffeine/items/77360dda05c8ce510084
    hyphens = '-˗ᅳ᭸‐‑‒–—―⁃⁻−▬─━➖ーㅡ﹘﹣－ｰ𐄐𐆑 '
    hyphens = '|'.join(hyphens)
    return re.sub(hyphens, replace_hyphen, text)


def katakana_to_hiragana(value):
    value = normalize(value)
    return ''.join([chr(ord(ch) - 96) if 'ァ' <= ch <= 'ヶ' else ch for ch in value])


def hiragana_to_katakana(value):
    value = normalize(value)
    return ''.join([chr(ord(ch) + 96) if 'ぁ' <= ch <= 'ゖ' else ch for ch in value])
