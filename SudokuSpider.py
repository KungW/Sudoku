#coding:utf-8
__author__ = 'Lyn  <tonylu716@gmail.com>'

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import time,pymysql,random
from threading import Thread


class SudokuSpider(Thread):
    '''
        该类用于爬取某数独网站的地图数据集，便于模型测试
    '''
    def __init__(self,need_web=True,visual=False):
        Thread.__init__(self)
        if need_web:
            if visual:
                self.driver = webdriver.Chrome()
            else:
                self.driver = webdriver.PhantomJS()
        else:
            pass

    def run(self):
        self.crawl_info_to_database()
        '''
        txt = file('maps/map_data_set.txt','a')
        self.crawl_info_to_txt(txt)
        '''

    def get_current_map_info(self,launched_by_select=False):
        '''得到当前页面上地图的一维数组形式'''
        browser = self.driver
        if not launched_by_select:
            while(1):
                try:
                    browser.get("http://www.llang.net/sudoku/type0.html")
                    if WebDriverWait(browser, 10).until(
                        EC.presence_of_element_located((By.XPATH,'//*[@id="sudokuform"]/center/table'))
                    ):
                        break
                except:
                    print('网页加载异常,重复访问...')
        blank_list = browser.find_element_by_xpath('//*[@id="sudokuform"]/center/table').find_elements_by_tag_name('input')
        value_list = map(lambda x:x.get_attribute('value'),blank_list)
        arr = []
        for i in value_list:
            if i:
                arr.append(i)
            else:
                arr.append('0')
        map_id = browser.find_element_by_xpath('//*[@id="NowSudoku"]').get_attribute('value')[1:-1].strip(' ')
        grade_S = Select(browser.find_element_by_xpath('//*[@id="sudokudiff"]'))
        grade = int(grade_S.all_selected_options[0].get_attribute('value'))
        return (arr,map_id,grade)

    def change_grade_and_fresh(self):
        browser = self.driver
        grade_S = Select(browser.find_element_by_xpath('//*[@id="sudokudiff"]'))
        grade_S.select_by_value(str(random.randint(0,5)))
        time.sleep(2)
        browser.find_element_by_xpath('//*[@id="anotherbutton"]').click()


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
        arr = self.get_current_map_info()[0]
        return self.arr_to_map_dict(arr)


    def crawl_info_to_txt(self,file):
        '''循环爬取地图，保存到文件中'''
        while(1):
            arr = self.get_current_map_info()[0]
            data_str = ','.join(arr)
            file.write(data_str+'\n')
            print(data_str+'write_success')


    def crawl_info_to_database(self):
        '''循环爬取地图，保存到数据库中'''
        conn = pymysql.connect(
            host='localhost',   port=3306,
            user='root',        passwd='',
            db='sudoku_maps',   charset='utf8'
        )
        cur = conn.cursor()
        launch_by_select = False
        while(1):
            info_tuple = self.get_current_map_info(launch_by_select)
            map_str = ','.join(info_tuple[0])
            print('map_id: {} , grade = {}'.format(info_tuple[1],info_tuple[2]))
            try:
                cur.execute(
                    "insert into maps(map_str,map_id,grade)"
                    "values (%s,%s,%s)",
                    (map_str,info_tuple[1],info_tuple[2])
                )
                conn.commit()
            except Exception as e:
                print(str(e))
            self.change_grade_and_fresh()
            launch_by_select = True


    def get_map_list_by_read_txt(self,file):
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


    def get_map_list_by_database(self,grade=None):
        cur = pymysql.connect(
            host='localhost',   port=3306,
            user='root',        passwd='',
            db='sudoku_maps',   charset='utf8'
        ).cursor()
        sql = "select map_str from maps "
        if grade!=None:
            sql += "where grade="+str(grade)
        cur.execute(sql)
        return map(lambda x:self.arr_to_map_dict(x[0].split(',')),cur.fetchall())


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
