import unittest

from django.core.exceptions import ValidationError

from ya_django_toolkit_jp.ja.validators.hiragana_only import \
    hiragana_only_validator


class TestValidator(unittest.TestCase):
    def test_hiragana_only_validator(self):
        self.assertIsNone(hiragana_only_validator('あいうえお'))
        self.assertRaises(
            ValidationError, lambda: hiragana_only_validator('カキクケコ'))


if __name__ == '__main__':
    unittest.main()
