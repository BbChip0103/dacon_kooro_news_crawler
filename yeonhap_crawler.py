# -*- coding: utf-8 -*-

import sys
from bs4 import BeautifulSoup
import requests
import re
import time
import json
import os
import os.path as pth


BASE_URL = "https://ars.yna.co.kr/api/v2/search"

def utf8_to_euckr(unicode_string):
    p = re.compile('\xc2|\xa0')
    text = p.sub('', unicode_string)
    text = text.encode('euc-kr', 'replace').decode('euc-kr')
    return text

def get_link_from_news_title(_keyword, _page_limit, _article_limit, _output_file, start_date, end_date):
    num_article = 0
    for pageno in range(_page_limit) :
        params = {
            'callback': 'Search.SearchPreCallback',
            'query': _keyword, # 검색할 키워드
            'scope': 'title', # all, title, 
            'ctype': 'A',
            'from': start_date,
            'to': end_date,
            'period':'diy',
            'page_no': pageno+1,
            'page_size':10,
            'channel':'basic_kr',
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
        }

        r = requests.get(BASE_URL, params=params, headers=headers)
        article_dict = json.loads(r.content[25:-2])
        r.close()

        article_id_list = article_dict['KR_ARTICLE']['result']
        if not article_id_list :
            break

        for article_id in article_id_list:
            contents_id = article_id['CONTENTS_ID']
            article_url = 'https://www.yna.co.kr/view/{}?section=search'.format(contents_id)
            try:
                get_text(article_url, _output_file)
                num_article += 1
            except:
                print('???')
            print(pageno, num_article)
            if num_article >= _article_limit:
                print('Num article :', num_article)
                return num_article

        print('Page Number :', pageno)		
    print('Num article :', num_article)
    return num_article


# 기사 본문 내용 긁어오기 (위 함수 내부에서 기사 본문 주소 받아 사용되는 함수)
def get_text(_article_url, output_file):
    r = requests.get(_article_url)
    soup = BeautifulSoup(r.content, 'lxml', from_encoding='utf-8')
    r.close()
    content_of_article = soup.find('div', class_='story-news')
    if content_of_article != None :
        text_list = content_of_article.find_all('p')
        for text in text_list :
            text = text.get_text()
            p = re.compile('\xc2|\xa0')
            text = p.sub('', text)

            p = re.compile('.+?@.+?\.co|.+?@.+?\.kr')
            matching = p.search(text)
            if matching != None :
                continue

            p = re.compile('저작권자|연합뉴스')
            matching = p.search(text)
            if matching != None :
                continue

            text = utf8_to_euckr(text)
            output_file.write(text)

        time.sleep(1)

# 메인함수
def main(argv):
    if len(argv) != 4:
        print("python [모듈이름] [키워드] [가져올 기사 수] [결과 파일명]")
        return

    # keyword = argv[1]
    keyword = '코로나' # argv[1]
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
