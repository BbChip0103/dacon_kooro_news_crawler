# -*- coding: utf-8 -*-

import sys
from bs4 import BeautifulSoup
import requests
import re
import time
import os
import os.path as pth


BASE_URL = 'http://nsearch.chosun.com/search/total.search'


def utf8_to_euckr(unicode_string):
    p = re.compile('\xc2|\xa0')
    text = p.sub('', unicode_string)
    text = text.encode('euc-kr', 'replace').decode('euc-kr')
    return text

def get_link_from_news_title(_keyword, _page_limit, _article_limit, _output_file, start_date, end_date) :
    num_article = 0
    for pageno in range(_page_limit) :
        params = {
            'query': _keyword, #검색할 키워드
            'pn': pageno+1, #페이지 번호
			'sort': 0, # 0: 관련도순, 1: 최신순
            'date_start': start_date,
            'date_end': end_date,
            # 'orderby':'news', 
            # 'categoryname': '조선일보',
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
            'Upgrade-Insecure-Requests': str(1),
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'ko,en-US;q=0.9,en;q=0.8',
        }

        r = requests.get(BASE_URL, params=params, headers=headers)
        soup = BeautifulSoup(r.content, 'lxml', from_encoding='utf-8')
        r.close()

        title_list = soup.find_all('dl', 'search_news')
        if(title_list == None) :
            break

        for title in title_list:
            article_title = title.dt.a.text

            if article_title.find('코로나') == -1:
                continue
            # if article_title.find('후유증') == -1:
            #     continue

            # print(article_title)

            article_url = title.dt.a['href']
            # print(len(title_list))
            get_text(article_url, _output_file)
            num_article += 1
            print(pageno, num_article)
            if num_article >= _article_limit:
                print('Num article :', num_article)
                return num_article
    
        print('Page Number :', pageno)		
    print('Num article :', num_article)
    return num_article


def get_text(_article_url, output_file):
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    r = requests.get(_article_url, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml', from_encoding='utf-8')
    r.close()
    content_of_article = soup.select('div.par')

    if content_of_article == None :
        content_of_article = soup.select('div.article')

    if content_of_article != None :
        for body in content_of_article :
            text_list = body.find_all(text=True, recursive=False)

            for text in text_list :
                p = re.compile('기자')
                matching = p.search(text)
                if matching != None and len(text) < 40 :
                    continue

                p = re.compile('.+?@.+?\.co|.+?@.+?\.kr')
                matching = p.search(text)
                if matching != None :
                    continue

                p = re.compile('\[.+?\]')
                m = p.search(text)
                if m != None :
                    text = text[m.end() : ]

                text = utf8_to_euckr(text)
                output_file.write(text)
                # print(text)

    time.sleep(1)

def main(argv):
    if len(argv) != 4:
        print("python [모듈이름] [키워드] [기사 수] [결과 파일경로]")
        return

    # keyword = argv[1]
    keyword = '코로나' # argv[1]
    page_limit = 100
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
