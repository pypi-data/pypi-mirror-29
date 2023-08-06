import re
from datetime import datetime

from .base import BaseParser
from .utils import norm
from .static import SupportedPages


class NewsParser(BaseParser):
    """Parser for news page"""
    URL = SupportedPages.NEWS.value

    def parse(self) -> dict:
        """
        Parse news and convert it to dict
        :return: { 'data': [
                {
                    'created_at': 掲載日,
                    'division': 発信課,
                    'category': 分類,
                    'detail': 詳細,
                    'title': タイトル,
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
        all_dl = self.soup.findAll("dl", attrs={'class': 'notice_list_dl'})
        rm_margin_regex = re.compile(r'(\s){2,}')
        for dl in all_dl:
            all_dd = dl.findAll('dd')
            if len(all_dd) == 0:
                # if not include dd
                continue
            # replace <br> with \n
            for e in all_dd[3].findAll('br'):
                e.replace_with('\n')
            # remove unnecessary margin
            sentence_list = []
            for sentence in all_dd[3].text.split('\n'):
                margin_removed_sentence = rm_margin_regex.sub('', sentence.strip())
                if len(margin_removed_sentence) == 0:
                    # if empty
                    continue
                sentence_list.append(margin_removed_sentence)
            result = {
                'created_at': datetime.strptime(norm(all_dd[0].text.strip()), '%Y.%m.%d'),
                'division': norm(all_dd[1].text.strip()),
                'category': norm(all_dd[2].text.strip()),
                'detail': '\n'.join(sentence_list),
                'title': sentence_list[0],
                'links': [
                    {'title': link.text.strip(), 'url': link.get('href')} for link in all_dd[3].findAll('a')
                ]
            }
            results['data'].append(result)
        return results
