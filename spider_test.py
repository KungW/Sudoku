#coding:utf-8
__author__ = 'Lyn  <tonylu716@gmail.com>'

from SudokuSpider import SudokuSpider
import time

for i in range(4):
    ss = SudokuSpider()
    ss.start()


while(1):
    time.sleep(3)
