#coding:utf-8
__author__ = 'Lyn  <tonylu716@gmail.com>'

from SudokuParser import SudokuParser
from SudokuSpider import SudokuSpider
import time


def get_current_map_answer(spider):
    #即时爬取网站地图，立刻求解，游戏外挂形式
    current_map = spider.get_current_map_dict()
    sudoku = SudokuParser(current_map)
    sudoku.parse()
    answer_arr = []
    if sudoku.answer_length==1:
        answer_arr = spider.map_dict_to_arr(sudoku.answer[0])
    return answer_arr


def crack():
    spider = SudokuSpider(need_web=True)
    while(1):
        answer_arr = get_current_map_answer(spider)
        print('answer:',answer_arr)
        if answer_arr:
            spider.fill_answer(answer_arr)

if __name__=='__main__':
    crack()