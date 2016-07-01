#coding:utf-8

__author__ = 'Tony Lu'

import random,time


class SudokuMapGenerator(object):
    def __init__(self,grade,txt=None):
        self.base_map = {
            0:  [0,0,0,0,0,0,0,0,0],
            1:  [0,0,0,0,0,0,0,0,0],
            2:  [0,0,0,0,0,0,0,0,0],
            3:  [0,0,0,0,0,0,0,0,0],
            4:  [0,0,0,0,0,0,0,0,0],
            5:  [0,0,0,0,0,0,0,0,0],
            6:  [0,0,0,0,0,0,0,0,0],
            7:  [0,0,0,0,0,0,0,0,0],
            8:  [0,0,0,0,0,0,0,0,0],
        }
        self.map = self.backup(self.base_map)
        self.grade = grade
        self.generator()

    def generator(self):
        foo = [1,1,1,1]
        for i in range(self.grade):
            foo.append(0)
        print(foo)
        cot = 0
        while(1):
            cot += 1
            try:
                for i in range(0,9):
                    for j in range(0,9):
                        #print(i,j,self.map[i][j])
                        if not self.map[i][j]:
                            '''对于所有的0格'''
                            potential_value_set = self.check_unit(i,j)
                            #print(potential_value_set)
                            #time.sleep(1)
                            if potential_value_set:
                                if random.choice(foo):
                                    if len(potential_value_set)>3:
                                        self.map[i][j] = random.choice(potential_value_set)
                                        if not self.building_map_check_before_ok:
                                            print(i,j)
                                            raise NameError('GenerateCheckBeforeError')
                                    else:
                                        for value in potential_value_set:
                                            self.map[i][j] = value
                                            if self.building_map_check_before_ok:
                                                break
                                else:
                                    self.map[i][j] = 0
                            else:
                                raise NameError('GenerateError')
                        #print(i,j,self.map[i][j])
                break
            except Exception as e:
                print(str(e),cot)
                print('--------------')
                self.map = self.backup(self.base_map)
        print('generate times:'+str(cot))
        #self.show()


    def check_unit(self,i,j):
        '''本函数检查该格是否仍有值可填（填过的也可以）'''
        potential_value_set = range(1,10)
        if self.map[i][j]:
            potential_value_set.remove(self.map[i][j])
        #搜索本行,本列，及所属田字，排除掉无效值，筛选出可能值列表
        self.search_row(i,potential_value_set)
        self.search_col(j,potential_value_set)
        self.search_field(j,i,potential_value_set)
        return potential_value_set

    @property
    def building_map_check_before_ok(self):
        '''检查地图所有已填格是否符合规则'''
        for i in range(0,9):
            for j in range(0,9):
                if self.map[i][j]:
                    if not self.check_unit(i,j):
                        #若之前填入的格子已无值可选，即填入的值有冲突，则表明生成失败
                        print(i,j,'check before failed')
                        return False
        return True

    def backup(self,extend_map=None):
        if extend_map:
            m = extend_map
        else:
            m = self.map
        save_map = {}#做备份
        for k in m.keys():
            #深度拷贝
            save_map[k] = []
            map(save_map[k].append,(m[k]))
        return save_map

    def search_row(self,i,potential_value_set):
        '''搜索行，排除无效值'''
        for ele in self.map[i]:
            if ele!=0:
                try:
                    potential_value_set.remove(ele)
                except:
                    pass
        #print 'search_row:',potential_value_set

    def search_col(self,j,potential_value_set):
        '''搜索列，排除无效值'''
        col_values = []
        for i in range(0,9):
            col_values.append(self.map[i][j])
        for ele in col_values:
            if ele!=0:
                try:
                    potential_value_set.remove(ele)
                except:
                    pass
        #print 'search_col:',potential_value_set


    def search_field(self,i,j,potential_value_set):
        '''搜索田字格，排除无效值'''
        field_values = []
        i_range = range(i/3*3,i/3*3+3)
        j_range = range(j/3*3,j/3*3+3)
        #print(i_range,j_range)
        for i in i_range:
            for j in j_range:
                field_values.append(self.map[j][i])
        for ele in field_values:
            if ele != 0:
                try:
                    potential_value_set.remove(ele)
                except:
                    pass
        #print 'search_field:',potential_value_set

    def show(self,extend_map=None):
        '''将内部或外部地图以友好的形式展示在控制台'''
        map = None
        if extend_map:
            map = extend_map
        else:
            map = self.map
        for i in range(0,9):
            row_str = ''
            for j in range(0,9):
                row_str += str(map[i][j])+' '
                if (j+1)%3==0:
                    row_str += '| '
            if (i)%3==0:
                print('------------------------')
            print(row_str)
