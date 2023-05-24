import unittest

from django.core.exceptions import ValidationError

from ya_django_toolkit_jp.ja.validators.katakana_only import \
    katakana_only_validator


class TestValidator(unittest.TestCase):
    def test_katakana_only_validator(self):
        self.assertIsNone(katakana_only_validator('アイウエオ'))
        self.assertRaises(
            ValidationError, lambda: katakana_only_validator('かきくけこ'))


if __name__ == '__main__':
    unittest.main()
