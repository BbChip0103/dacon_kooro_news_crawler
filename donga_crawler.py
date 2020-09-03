# -*- coding: utf-8 -*-

import sys
from bs4 import BeautifulSoup
import requests
import re
import time


BASE_URL = "http://news.donga.com/search"

def get_link_from_news_title(_keyword, _page_limit, _output_file):
    for i in range(_page_limit) :
        params = {
            'p': str(1 + i*15), #페이지 번호
            'query': _keyword, #검색할 키워드
            'check_news':'1', #정렬 순서(최신순)
            'more': '1',
            'sorting': '1',
            'range': '1', # 1: 전체, 2: 제목
            'search_date': '2' # 2: 1년 안에꺼만
        }

        r = requests.get(BASE_URL, params)
        soup = BeautifulSoup(r.content, 'lxml', from_encoding='utf-8')
        r.close()

        title_list = soup.find_all('p', 'tit')
        if(title_list == None) :
            break;

        for title in title_list:
            article_title = title.a.get_text(strip=True)
            # print(article_title)
            # p = re.compile('[.*?인사.*?]')
            # matching = p.search(article_title)
            # if(matching != None) :
            #     continue

            article_url = title.a['href']
            # print(article_url)
            get_text(article_url, _output_file)

        print('Page Number :', i)


# 기사 본문 내용 긁어오기 (위 함수 내부에서 기사 본문 주소 받아 사용되는 함수)
def get_text(_article_url, output_file):
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    r = requests.get(_article_url, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml', from_encoding='utf-8')
    r.close()
    content_of_article = soup.select('div.article_txt')

    if content_of_article != None :
        text_list = content_of_article[0].find_all(text=True, recursive=False)

        for text in text_list :
            p = re.compile('\xc2|\xa0')
            text = p.sub('', text)

            # p = re.compile('.+?\s기자\s.+?@.+?\.com|.+?\s기자\s.+?@.+?\.co.kr')
            # matching = p.sub('', text)

            p = re.compile('기자')
            matching = p.search(text)

            if matching != None and len(text) < 40 :
                continue;

            p = re.compile('.+?@.+?\.co|.+?@.+?\.kr')
            matching = p.search(text)

            if matching != None :
                continue;

            text = text.encode('euc-kr', 'replace').decode('euc-kr')
            output_file.write(text)

        time.sleep(1)

# 메인함수
def main(argv):
    if len(argv) != 4:
        print("python [모듈이름] [키워드] [가져올 페이지 숫자] [결과 파일명]")
        return

    # keyword = argv[1]
    keyword = '코로나 후유증 합병증' # argv[1]
    page_limit = int(argv[2])
    output_file_name = argv[3]

    output_file = open(output_file_name, 'w')
    get_link_from_news_title(keyword, page_limit, output_file)
    output_file.close()


if __name__ == '__main__':
    main(sys.argv)
