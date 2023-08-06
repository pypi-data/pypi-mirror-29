from unittest import TestCase
from nose.tools import eq_, raises
from student_portal_crawler.parser import norm, get_key_from_url


class TestNormalize(TestCase):
    """Test case for `utils.norm`"""

    def test_normal_text(self):
        """Normal text test for `utils.norm`"""
        immutable_text = 'hogefuga'
        eq_(norm(immutable_text), immutable_text)

    def test_half_width_text(self):
        """Half-width katakana text test for `utils.norm`"""
        mutable_text = 'ｱｲｳｴｵ'
        expected_text = 'アイウエオ'
        eq_(norm(mutable_text), expected_text)

    def test_not_separated_dullness_text(self):
        """Dullness or half-dullness combined text test for `utils.norm`"""
        combined_text = 'ガギグゲゴ'
        eq_(norm(combined_text), combined_text)
        combined_text = 'パピプペポ'
        eq_(norm(combined_text), combined_text)

    def test_separated_dullness_text(self):
        """Dullness or half-dullness separated text test for `utils.norm`"""
        separated_text = 'ｶﾞｷﾞｸﾞｹﾞｺﾞｳﾞｧう゛'
        eq_(norm(separated_text), 'ガギグゲゴヴァう ゙')
        separated_text = 'ﾊﾟﾋﾟﾌﾟﾍﾟﾎﾟほ゜'
        eq_(norm(separated_text), 'パピプペポほ ゚')


class TestGetKeyFromUrl(TestCase):
    """Test case for `parser.get_key_from_url`"""

    def test_valid_url(self):
        """Valid URL test for `utils.get_key_from_url`"""
        valid_url = 'https://www.example.com/'
        eq_(get_key_from_url(valid_url), valid_url)

    @raises(ValueError)
    def test_scheme_missing_url(self):
        """Invalid URL (scheme missing) URL test for `utils.get_key_from_url`"""
        scheme_missing_url = 'www.example.com'
        get_key_from_url(scheme_missing_url)

    @raises(ValueError)
    def test_netloc_missing_url(self):
        """Invalid URL (netloc missing) URL test for `utils.get_key_from_url`"""
        netloc_missing_url = 'https://'
        get_key_from_url(netloc_missing_url)
