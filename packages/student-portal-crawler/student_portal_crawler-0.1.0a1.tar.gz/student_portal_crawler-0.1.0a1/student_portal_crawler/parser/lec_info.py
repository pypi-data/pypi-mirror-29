import re
from datetime import datetime

from .base import BaseParser
from .utils import norm
from .static import SupportedPages


class LectureInformationParser(BaseParser):
    """Parser for lecture information page"""
    URL = SupportedPages.LECTURE_INFORMATION.value

    def parse(self) -> dict:
        """
        Parse lecture information and convert it to dict
        :return: { 'data': [
                {
                    'grade': 学年,
                    'semester': 学期,
                    'lecture': 科目名,
                    'instructor': 講師名,
                    'week': 曜日,
                    'period': 時限,
                    'category': 分類,
                    'detail': 詳細,
                    'created_at': 初回掲載日,
                    'updated_at': 最終更新日,
                    'links': [
                        {
                            'title': '詳細に含まれるリンクのタイトル',
                            'url': '詳細に含まれるリンクのURL'
                        }
                    ]
                }
            ]
        }
        """
        results = dict()
        results['data'] = list()
        all_tr = self.soup.findAll('tr', attrs={'class': re.compile('^gen_tbl1_(even|odd)$')})
        for tr in all_tr:
            td_list = tr.findAll('td')
            norm_td_list = [norm(td.get_text()) for td in td_list]
            result = {
                'grade': norm_td_list[1],
                'semester': norm_td_list[2],
                'lecture': norm_td_list[3],
                'instructor': norm_td_list[4],
                'week': norm_td_list[5],
                'period': norm_td_list[6],
                'category': norm_td_list[7],
                'detail': norm_td_list[8].strip().replace('\t', ''),
                'created_at': datetime.strptime(norm_td_list[9], '%Y/%m/%d'),
                'updated_at': datetime.strptime(norm_td_list[10], '%Y/%m/%d'),
                'links': [
                    {'title': link.text.strip(), 'url': link.get('href')} for link in td_list[8].findAll('a')
                ]
            }
            results['data'].append(result)
        return results
