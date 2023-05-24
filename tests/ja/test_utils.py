import unittest

from ya_django_toolkit_jp.ja import utils


class TestUtilsMethods(unittest.TestCase):
    def test_remove_control_characters(self):
        self.assertEqual(utils.remove_control_characters('a\0b'), 'ab')
        self.assertEqual(utils.remove_control_characters('a\fb'), 'ab')
        self.assertEqual(utils.remove_control_characters('a\nb'), 'ab')
        self.assertEqual(utils.remove_control_characters('a\rb'), 'ab')
        self.assertEqual(utils.remove_control_characters('a\tb'), 'ab')
        self.assertEqual(utils.remove_control_characters('a\vb'), 'ab')

    def test_unicode_normalize(self):
        self.assertEqual(utils.unicode_normalize('ｱｲｳｴｵ'), 'アイウエオ')
        self.assertEqual(utils.unicode_normalize('ｶﾞｷﾞｸﾞｹﾞｺﾞ'), 'ガギグゲゴ')
        # 半角濁点
        self.assertEqual(utils.unicode_normalize('サﾞシﾞスﾞセﾞソﾞ'), 'ザジズゼゾ')
        # 全角濁点
        self.assertEqual(utils.unicode_normalize('サ゛シ゛ス゛セ゛ソ゛'), 'サ ゙シ ゙ス ゙セ ゙ソ ゙')  # noqa: E501
        # 濁点(12441)
        self.assertEqual(utils.unicode_normalize('サ ゙シ ゙ス ゙セ ゙ソ ゙'), 'サ ゙シ ゙ス ゙セ ゙ソ ゙')  # noqa: E501
        # unicode 濁点
        self.assertEqual(utils.unicode_normalize('ザジズゼゾ'), 'ザジズゼゾ')
        self.assertEqual(utils.unicode_normalize('ダヂヅデド'), 'ダヂヅデド')
        self.assertEqual(utils.unicode_normalize('髙'), '髙')
        self.assertEqual(utils.unicode_normalize('å'), 'å')

    def test_normalize(self):
        self.assertEqual(utils.normalize('ｱ\0ｲｳｴｵ'), 'アイウエオ')
        self.assertEqual(utils.normalize('ｶﾞ\fｷﾞｸﾞｹﾞｺﾞ'), 'ガギグゲゴ')
        self.assertEqual(utils.normalize('\nサﾞシﾞスﾞセﾞソﾞ'), 'ザジズゼゾ')
        self.assertEqual(utils.normalize('\rダヂヅデド'), 'ダヂヅデド')
        self.assertEqual(utils.normalize('\t髙'), '髙')
        self.assertEqual(utils.normalize('\vå'), 'å')

    def test_replace_hyphen(self):
        self.assertEqual(utils.replace_hyphen('a-b'), 'a-b')
        self.assertEqual(utils.replace_hyphen('a˗b'), 'a-b')
        self.assertEqual(utils.replace_hyphen('aᅳb'), 'a-b')
        self.assertEqual(utils.replace_hyphen('a᭸b'), 'a-b')
        self.assertEqual(utils.replace_hyphen('a‐b'), 'a-b')
        self.assertEqual(utils.replace_hyphen('a‑b'), 'a-b')
        self.assertEqual(utils.replace_hyphen('a‒b'), 'a-b')
        self.assertEqual(utils.replace_hyphen('a–b'), 'a-b')
        self.assertEqual(utils.replace_hyphen('a—b'), 'a-b')
        self.assertEqual(utils.replace_hyphen('a―b'), 'a-b')
        self.assertEqual(utils.replace_hyphen('a⁃b'), 'a-b')
        self.assertEqual(utils.replace_hyphen('a⁻b'), 'a-b')
        self.assertEqual(utils.replace_hyphen('a−b'), 'a-b')
        self.assertEqual(utils.replace_hyphen('a▬b'), 'a-b')
        self.assertEqual(utils.replace_hyphen('a─b'), 'a-b')
        self.assertEqual(utils.replace_hyphen('a━b'), 'a-b')
        self.assertEqual(utils.replace_hyphen('a➖b'), 'a-b')
        self.assertEqual(utils.replace_hyphen('aーb'), 'a-b')
        self.assertEqual(utils.replace_hyphen('aㅡb'), 'a-b')
        self.assertEqual(utils.replace_hyphen('a﹘b'), 'a-b')
        self.assertEqual(utils.replace_hyphen('a﹣b'), 'a-b')
        self.assertEqual(utils.replace_hyphen('a－b'), 'a-b')
        self.assertEqual(utils.replace_hyphen('aｰb'), 'a-b')
        self.assertEqual(utils.replace_hyphen('a𐄐b'), 'a-b')
        self.assertEqual(utils.replace_hyphen('a𐆑b'), 'a-b')
        self.assertEqual(utils.replace_hyphen('a b'), 'a-b')
        self.assertEqual(utils.replace_hyphen('a一b'), 'a一b')

    def test_katakana_to_hiragana(self):
        self.assertEqual(utils.katakana_to_hiragana('アイウエオ'), 'あいうえお')
        self.assertEqual(utils.katakana_to_hiragana('ｶﾞｷﾞｸﾞｹﾞｺﾞ'), 'がぎぐげご')
        self.assertEqual(utils.katakana_to_hiragana('サﾞシﾞスﾞセﾞソﾞ'), 'ざじずぜぞ')
        self.assertEqual(utils.katakana_to_hiragana('たちつてと'), 'たちつてと')

    def test_hiragana_to_katakana(self):
        self.assertEqual(utils.hiragana_to_katakana('あいうえお'), 'アイウエオ')
        self.assertEqual(utils.hiragana_to_katakana('がぎぐげご'), 'ガギグゲゴ')
        self.assertEqual(utils.hiragana_to_katakana('さﾞしﾞすﾞせﾞそﾞ'), 'ザジズゼゾ')


if __name__ == '__main__':
    unittest.main()
