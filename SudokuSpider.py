#coding:utf-8
__author__ = 'Administrator'

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class SudokuSpider(object):
    '''
        该类用于爬取某数独网站的地图数据集，便于模型测试
    '''
    def __init__(self,need_web=True):
        if need_web:
            self.driver = webdriver.Chrome()
        else:
            pass

    def get_current_arr(self):
        '''得到当前页面上地图的一维数组形式'''
        browser = self.driver
        while(1):
                browser.get("http://www.llang.net/sudoku/type0.html")
                try:
                    if WebDriverWait(browser, 10).until(
                        EC.presence_of_element_located((By.XPATH,'//*[@id="sudokuform"]/center/table'))
                    ):
                        break
                except:
                    print('网页加载异常,重复访问...')
        ele = browser.find_element_by_xpath('//*[@id="sudokuform"]/center/table')
        blank_list = ele.find_elements_by_tag_name('input')
        value_list = map(lambda x:x.get_attribute('value'),blank_list)
        arr = []
        for i in value_list:
            if i:
                arr.append(i)
            else:
                arr.append('0')
        return arr


    def fill_answer(self,answer_arr):
        browser = self.driver
        blank_list = browser.find_element_by_xpath('//*[@id="sudokuform"]/center/table').find_elements_by_tag_name('input')
        cot = 0
        print('开始破解！')
        for blank in blank_list:
            blank.send_keys(str(answer_arr[cot]))
            print('数据注入: '+str(cot)+' —— '+str(answer_arr[cot]))
            cot += 1
        browser.find_element_by_xpath('//*[@id="toolspanel"]/div[1]/center/input[4]').click()
        time.sleep(15)

    def get_current_map_dict(self):
        '''得到当前页面的地图，直接传给模型，用于即时外挂'''
        arr = self.get_current_arr()
        return self.arr_to_map_dict(arr)


    def crawl_info_to(self,file):
        '''循环爬取地图，保存到文件中'''
        while(1):
            arr = self.get_current_arr()
            data_str = ','.join(arr)
            file.write(data_str+'\n')
            print(data_str+'write_success')


    def get_map_list_by_read(self,file):
        '''读取保存的地图，用于测试模型'''
        map_list = []
        while 1:
            line = file.readline()
            #print(line)
            if not line:
                break
            arr = line.split(',')
            #print(arr)
            map_list.append(self.arr_to_map_dict(arr))
        print('Read success,get {} maps'.format(len(map_list)))
        return map_list


    def arr_to_map_dict(self,arr):
        '''处理爬取到的一维数组为二维数组形式，传给解析模型'''
        map_dict = {
            0:  [5,0,0,0,9,0,2,0,1],
            1:  [0,0,2,0,0,7,0,0,8],
            2:  [0,8,0,0,0,0,3,0,0],
            3:  [0,1,4,0,0,5,0,0,0],
            4:  [0,0,0,9,0,3,0,0,0],
            5:  [0,0,0,8,0,0,9,4,0],
            6:  [0,0,3,0,0,0,0,6,0],
            7:  [6,0,0,2,0,0,1,0,0],
            8:  [8,0,9,0,6,0,0,0,5],
        }
        cot = 0
        for i in range(len(arr)):
            map_dict[cot][i%9] = int(arr[i])
            if not (i+1)%9:
                cot += 1
        return map_dict

    def map_dict_to_arr(self,map_dict):
        arr = []
        for key in map_dict.keys():
            row = map_dict[key]
            for j in range(len(row)):
                arr.append(str(map_dict[key][j]))
        return arr

    def map_dict_to_str(self,map_dict):
        return ','.join(self.map_dict_to_arr(map_dict))
