import os
import unittest
import codecs

from datetime import datetime
from nose.tools import ok_, eq_
from bs4 import BeautifulSoup
from student_portal_crawler.parser import LectureInformationParser


class LectureInformationParserTest(unittest.TestCase):
    """Test case for LectureInformationParser"""

    SAMPLE_DATE = datetime(2018, 2, 7)
    RESULT_DATA_SET = [
        {
            'grade': '学部',
            'semester': '後',
            'lecture': '工繊入門',
            'instructor': '工繊一郎',
            'week': '水曜日',
            'period': '2',
            'category': 'レポート・課題',
            'detail': 'おしらせ\nsample link',
            'created_at': SAMPLE_DATE,
            'updated_at': SAMPLE_DATE,
            'links': [
                {
                    'title': 'sample link',
                    'url': 'https://example.com/'
                }
            ]
        },
        {
            'grade': '学部',
            'semester': '後',
            'lecture': '工繊実践',
            'instructor': '工繊二郎',
            'week': '集中',
            'period': '-',
            'category': 'レポート・課題',
            'detail': 'おしらせ\nsample link',
            'created_at': SAMPLE_DATE,
            'updated_at': SAMPLE_DATE,
            'links': [
                {
                    'title': 'sample link',
                    'url': 'https://example.com/'
                }
            ]
        },
        {
            'grade': '学部',
            'semester': '-',
            'lecture': '工繊応用',
            'instructor': '工繊三郎',
            'week': '-',
            'period': '-',
            'category': 'その他',
            'detail': 'テストテスト',
            'created_at': SAMPLE_DATE,
            'updated_at': SAMPLE_DATE,
            'links': []
        }
    ]

    @classmethod
    def setUpClass(cls):
        sample_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'samples')
        with codecs.open(os.path.join(sample_dir_path, 'information.html'), 'r', encoding='utf-8') as fp:
            cls.HTML = fp.read()

    def test_normal_response(self):
        """Normal response test for LectureInformationParser"""
        parser = LectureInformationParser(self.HTML)
        data = parser.parse()
        ok_(type(data), dict)
        ok_('data' in data.keys())
        eq_(len(data['data']), 3)
        for expected_result, actual_result in zip(self.RESULT_DATA_SET, data['data']):
            eq_(expected_result, actual_result)

    def test_empty_response(self):
        """Empty response test for LectureInformationParser"""
        parser = LectureInformationParser('')
        data = parser.parse()
        ok_(type(data), dict)
        ok_('data' in data.keys())
        eq_(len(data['data']), 0)
