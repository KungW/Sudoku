#coding:utf-8

__author__ = 'Tony Lu'

from SudokuSpider import SudokuSpider

import time,pymysql


conn = pymysql.connect(
    host='localhost',   port=3306,
    user='root',        passwd='',
    db='sudoku_maps',   charset='utf8'
)


for i in range(4):
    ss = SudokuSpider()
    ss.start()


while(1):
    time.sleep(3)
