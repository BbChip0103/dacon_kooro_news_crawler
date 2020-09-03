#-*-coding: utf-8

from collections import Counter
from konlpy.tag import Okt

FONT_PATH = '/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf'

with open('donga_corona.txt', 'r') as f:
    text = f.read()

spliter = Okt()
nouns = spliter.nouns(text)
nouns = [word for word in nouns if len(word) >= 2]

# stop_words = ['서울', '기자']
# nouns = [each_word for each_word in nouns if each_word not in stop_words]

cnt = Counter(nouns).most_common(200)
# dic_cnt = dict(cnt)

for word in cnt:
    print(word)
