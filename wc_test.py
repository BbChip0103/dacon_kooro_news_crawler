#-*-coding: utf-8

import os
from os import path as pth
from PIL import Image
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import random
from konlpy.tag import Okt
from wordcloud import WordCloud

def color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    #return "hsl(221, %d%%, %d%%)" %(random.randint(40, 50), random.randint(40, 50))
    return "hsl(0, %d%%, %d%%)" %(random.randint(0, 10), random.randint(90, 100))

    #return "hsl(0, 0%, 100%)"


FONT_PATH = 'C:/Windows/Fonts/BMJUA_ttf.ttf'

target_base_path = 'merged_result'
result_base_path = 'wc_result'
os.makedirs(result_base_path, exist_ok=True)

for month_i in range(8):
    start_date = '2020{:02d}01'.format(month_i+1)
    end_date = '2020{:02d}01'.format(month_i+2)
    target_filename = pth.join(target_base_path, '{}_{}_{}'.format(start_date, end_date, 'merged_news.txt'))
    with open(target_filename) as f:
        text = f.read()

    spliter = Okt()
    nouns = spliter.nouns(text)

    list_end = len(nouns)
    i = 0
    while i < list_end :
        if len(nouns[i]) == 1 :
            nouns.remove(nouns[i])
            list_end -= 1
        else :
            i += 1


    stop_words = [ ]
    # stop_words = ['코로나', '후유증', '합병증', ]
    # stop_words = []
    nouns = [each_word for each_word in nouns if each_word not in stop_words]

    cnt = Counter(nouns).most_common(200)
    dic_cnt = dict(cnt)

    # read the mask image
    # taken from
    MASK = np.array(Image.open(pth.join("jammanbo_mask.png")))

    wc = WordCloud(
        font_path=FONT_PATH, 
        background_color="black",
        max_words=200,
        mask=MASK,
        width=1000, 
        height=1000,
        color_func=color_func,
    )

    # generate word cloud
    wc.generate_from_frequencies(dic_cnt)

    # store to file
    wc.to_file(pth.join(result_base_path, "result.png"))

    '''
    # show
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.figure()
    plt.imshow(MASK, cmap=plt.cm.gray, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    '''
