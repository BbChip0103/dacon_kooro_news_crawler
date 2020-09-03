# -*- coding: utf-8 -*-

import sys
from bs4 import BeautifulSoup
import requests
import re
import time
import os
import os.path as pth


BASE_URL = 'http://news.joins.com/Search/TotalNews'


def utf8_to_euckr(unicode_string):
    p = re.compile('\xc2|\xa0')
    text = p.sub('', unicode_string)
    text = text.encode('euc-kr', 'replace').decode('euc-kr')
    return text

def get_link_from_news_title(_keyword, _page_limit, _article_limit, _output_file, start_date, end_date) :
    num_article = 0
    start_date = '{}.{}.{}'.format(start_date[:4], start_date[4:6], start_date[6:])
    end_date = '{}.{}.{}'.format(end_date[:4], end_date[4:6], end_date[6:])
    for pageno in range(_page_limit) :
        params = {
            'page': pageno+1, #페이지 번호
            'Keyword': _keyword, #검색할 키워드
            'SortType':'Accuracy', # New:정렬 순서(최신순), Accuracy:
            'ScopeType': 'Title',
            'SourceGroupType': 'Joongang',
            'SearchCategoryType': 'TotalNews',
            'PeriodType':'DirectInput',
            'StartSearchDate': start_date, # '2020.01.01',
            'EndSearchDate': end_date, # '2020.08.23',
        }
        r = requests.get(BASE_URL, params)
        soup = BeautifulSoup(r.content, 'lxml', from_encoding='utf-8')
        r.close()

        title_list = soup.find_all('h2', 'headline mg')
        if title_list == None :
            break

        for title in title_list:
            article_title = title.a.get_text(strip=True)
            # print(len(title_list))
            article_url = title.a['href']
            get_text(article_url, _output_file)
            num_article += 1
            print(pageno, num_article)
            if num_article >= _article_limit:
                print('Num article :', num_article)
                return num_article

        print('Page Number :', pageno)
    print('Num article :', num_article)
    return num_article


# 기사 본문 내용 긁어오기 (위 함수 내부에서 기사 본문 주소 받아 사용되는 함수)
def get_text(_article_url, output_file):
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    r = requests.get(_article_url, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml', from_encoding='utf-8')
    r.close()
    content_of_article = soup.select('div.article_body')


    if content_of_article != None :
        text_list = content_of_article[0].find_all(text=True, recursive=False)

        for text in text_list :
            p = re.compile('기자')
            matching = p.search(text)

            if matching != None and len(text) < 40 :
                continue

            p = re.compile('.+?@.+?\.co|.+?@.+?\.kr')
            matching = p.search(text)

            if matching != None :
                continue

            p = re.compile('아티클 공통')
            matching = p.search(text)

            if matching != None :
                break

            text = utf8_to_euckr(text)
            output_file.write(text)
            # print(text)

    time.sleep(1)


def main(argv):
    if len(argv) != 4:
        print("python [모듈이름] [키워드] [가져올 기사 수] [결과 파일명]")
        return

    # keyword = argv[1]
    keyword = '코로나'
    page_limit = 50
    article_limit = int(argv[2])
    output_file_name = argv[3]

    num_article_list = []
    output_base_path = 'result'
    os.makedirs(output_base_path, exist_ok=True)
    for month_i in range(8):
        start_date = '2020{:02d}01'.format(month_i+1)
        end_date = '2020{:02d}01'.format(month_i+2)
        output_filename = pth.join(output_base_path, '{}_{}_{}'.format(start_date, end_date, output_file_name))
        with open(output_filename, 'w') as output_file:
            num_article = get_link_from_news_title(keyword, page_limit, article_limit, output_file, start_date, end_date)
            num_article_list.append(num_article)
        print()
    print(num_article_list)


if __name__ == '__main__':
    main(sys.argv)
