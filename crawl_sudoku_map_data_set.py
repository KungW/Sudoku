#coding:utf-8

__author__ = 'Administrator'

from SudokuSpider import SudokuSpider

ss = SudokuSpider()

txt = file('a.txt','a')

ss.crawl_info_to(txt)
