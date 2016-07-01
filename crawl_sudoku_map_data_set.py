#coding:utf-8

__author__ = 'Tony Lu'

from SudokuSpider import SudokuSpider

ss = SudokuSpider()

txt = file('a.txt','a')

ss.crawl_info_to(txt)
