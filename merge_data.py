# -*- coding: utf-8 -*-

import sys
import os
import os.path as pth

# 메인함수
def main(argv):
    if len(argv) < 4:
        print("argument는 최소 4개 이상이어야 합니다.")
        print("마지막 인자는 출력파일명으로 해주세요.")
        print("ex\) python merge_data.py donga.txt chosun.txt jungang.txt merged_data.txt")
        return

    target_base_path = 'result'
    output_base_path = 'merged_result'
    os.makedirs(output_base_path, exist_ok=True)

    for month_i in range(8):
        start_date = '2020{:02d}01'.format(month_i+1)
        end_date = '2020{:02d}01'.format(month_i+2)
        output_filename = pth.join(output_base_path, '{}_{}_{}'.format(start_date, end_date, argv[-1]))
        with open(output_filename, 'w') as output_file:
            for file_name in argv[1:-1]:
                with open(pth.join(target_base_path, '{}_{}_{}'.format(start_date, end_date, file_name)), 'r') as article_file:
                    text = article_file.read()
                    output_file.write(text)
                    output_file.write('\n')

if __name__ == '__main__':
    main(sys.argv)
