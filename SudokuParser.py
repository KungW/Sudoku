#coding:utf-8

__author__ = 'Lyn  <tonylu716@gmail.com>'

from SudokuMapGenerator import SudokuMapGenerator
import time

class SudokuParser(object):
    '''
        该类用于数独题目的破解
    '''
    def __init__(self,map_dict=None,txt=None):
        if map_dict:
            self.map = map_dict
        else:
            self.map = SudokuMapGenerator(grade=3).map
            self.show()
            time.sleep(10)
        self.answer = []


    def parse(self,back_up=None):
        '''主推理递归函数，会生成搜索树'''
        #print('\n\n---------------------enter parse----------------')
        record_list = []
        try:
            '''尝试生成关于每个未填格的信息列表'''
            record_list = self.generate_record_list()
        except RuntimeError as e:
            if str(e)=='empty':
                #print('have empty value set! route failed')
                if back_up:
                    self.map = back_up
                return False
            else:
                #print('parse() Error:'+str(e))
                pass

        if record_list:
            for record in record_list:
                #print(record)
                pass
        else:
            '''已经没有未填格子，做最后检验'''
            if self.success:
                self.answer.append(self.backup())
                return True
            else:
                '''每一步都有检验，不太可能失败，纯粹为逻辑严谨性'''
                return False

        '''根据record_list把已经推断出的直接填上'''
        if not self.fill_certain_values(record_list,back_up):
            return False

        '''试值递归函数，会重复调用parse，开辟新分支'''
        if not self.try_values(record_list):
            return False

        #print('---------------------end parse----------------\n\n')
        if self.success:
            self.answer.append(self.backup())
            return True
        return False


    def generate_record_list(self):
        '''
            生成一个关于每一个未完成格子的信息列表
            单位元素内，包含其坐标信息以及可能值列表
            为减小推理开销
            需要将此信息列表按可能值数量降序排列
        '''
        #print('***************generate_record_list*************************')
        record_list = []
        for i in range(0,9):
            for j in range(0,9):
                ##print i,j,self.map[i][j]
                if self.map[i][j]==0:
                    potential_value_set = range(1,10)
                    #搜索本行,本列，及所属田字，排除掉无效值，筛选出可能值列表
                    self.search_row(i,potential_value_set)
                    self.search_col(j,potential_value_set)
                    self.search_field(j,i,potential_value_set)
                    set_length = len(potential_value_set)
                    if set_length==0:
                        raise RuntimeError('empty')
                    record = {
                        'i':            i,
                        'j':            j,
                        'value_set':    potential_value_set,
                        'set_length':   set_length
                    }
                    record_list.append(record)
        return sorted(record_list,key=lambda s:s['set_length'])


    def fill_certain_values(self,record_list,back_up):
        '''把已经推断出的直接填上'''
        #print('***************fill certain values*************************')
        for record in record_list:
            if record['set_length']==1:
                #print(record)
                self.map[record['i']][record['j']] = list(record['value_set'])[0]
                if not self.check_unit(record['i'],record['j']):
                    #print('this only left value is not ok!Back up!')
                    self.map = back_up
                    return False
        return True


    def try_values(self,record_list):
        '''试值递归,重复调用parse函数，开辟新分支'''
        #print('***************try values*************************')
        for record in record_list:
            if record['set_length']>=2:
                #print '\nrecord:',record
                flag = 0
                for possible_value in list(record['value_set']):
                    #print 'let self.map [',str(record['i']),',',str(record['j']),'] = ',possible_value
                    '''map更替前备份'''
                    back_up = self.backup()
                    self.map[record['i']][record['j']] = possible_value
                    if self.check_unit(record['i'],record['j']):
                        '''对于每一个新生成的上层节点做基本判断，若他自身都不行，则他的整个分支不需要考虑'''
                        flag = 1
                        if self.parse(back_up):
                            '''
                                如果此路径已经走通了，不要急于return，排除其他路径，
                                如果是一解题，会出现殊途同归的情况，多解也不漏
                            '''
                            break
                if not flag:
                    '''如果条目中有一条record的所有possible_value都为无效路径，则说明上层推理有误，节点回溯'''
                    return False
        return True


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

    def backup(self,extend_map=None):
        '''深度拷贝地图，做备份'''
        if extend_map:
            m = extend_map
        else:
            m = self.map
        save_map = {}
        for k in m.keys():
            save_map[k] = []
            map(save_map[k].append,(m[k]))
        return save_map

    @property
    def multi_answer(self):
        '''返回是否多解，假如False，则有可能无解或单解'''
        if len(self.answer)==0:
            return False
        multi_answer = False
        for i in range(0,len(self.answer)):
            try:
                if self.answer[i]!=self.answer[i+1]:
                    multi_answer = True
                    print('multi_answer:')
                    self.show(self.answer[i])
                    print('--------------------')
                    self.show(self.answer[i+1])
            except:
                pass
        return multi_answer

    @property
    def answer_length(self):
        '''
            用于获得解的数目，
            注意：len(self.answer)不等同于该结果
            self.answer是列表，有元素重复
        '''
        if not self.multi_answer:
            if len(self.answer):
                return 1
            else:
                return 0
        #多解长度之后用set写一写
        return -1


    def show_result(self):
        print('\n------result-----------')
        if not self.multi_answer:
            #非多解，则可能为1解或无解
            if len(self.answer):
                print('\n\n\nNo multi_answer')
                print ('find {} routes ,get 1 answer:'.format(str(len(self.answer))))
                self.show(self.answer[0])
            else:
                print('no answer')


    def check_unit(self,i,j):
        '''检查单位格子是否符合规则'''
        value = self.map[i][j]
        for v in range(0,9):
            if v!=j:
                ##print(self.map[i][v])
                if value == self.map[i][v]:
                    #print 'ROW check_unit Error,equal with = (',str(i),',',str(v),')'
                    return False
        for k in range(0,9):
            if k!=i:
                ##print(self.map[k][j])
                if value == self.map[k][j]:
                    #print 'COL check_unit Error,equal with = (',str(k),',',str(j),')'
                    return False
        i_range = range(i/3*3,i/3*3+3)
        j_range = range(j/3*3,j/3*3+3)
        for I in i_range:
            for J in j_range:
                if  I!=i or J!=j:
                    ##print self.map[I][J]
                    if value == self.map[I][J]:
                        #print 'FIELD check_unit Error,equal with = (',str(I),',',str(J),')'
                        return False
        return True

    @property
    def success(self):
        '''检查地图所有格子是否符合规则'''
        for i in range(0,9):
            for j in range(0,9):
                if not self.check_unit(i,j):
                    #print 'in (',str(i),',',str(j),')false!','value = ',self.map[i][j]
                    #print('please see that:')
                    #self.show()
                    return False
        #print('check_success!!!')
        return True

    def search_row(self,i,potential_value_set):
        '''搜索行，排除无效值'''
        for ele in self.map[i]:
            if ele!=0:
                try:
                    potential_value_set.remove(ele)
                except:
                    pass
        ##print 'search_row:',potential_value_set

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
        ##print 'search_col:',potential_value_set


    def search_field(self,i,j,potential_value_set):
        '''搜索田字格，排除无效值'''
        field_values = []
        i_range = range(i/3*3,i/3*3+3)
        j_range = range(j/3*3,j/3*3+3)
        ##print(i_range,j_range)
        for i in i_range:
            for j in j_range:
                field_values.append(self.map[j][i])
        for ele in field_values:
            if ele != 0:
                try:
                    potential_value_set.remove(ele)
                except:
                    pass
        ##print 'search_field:',potential_value_set







    '''
    def backup(self):
        save_map = {}#做备份
        for k in self.map.keys():
            save_map[k] = self.map[k]
            #这样拷贝不行，浅拷贝会用到原本的数组指针
            #备份的就一直在随他变化，起不到备份作用
        return save_map
    '''

    '''
    def main_parse(self,index=1):
        flag = 1
        record_list = []
        #能用逻辑推断的全用逻辑推断
        while(flag):
            record_list = self.generate_record_list()
            for record in record_list:
                #print(record)
                if record['set_length']==1:
                    self.map[record['i']][record['j']] = list(record['value_set'])[0]
                else:
                    flag = 0
        #不能的用暴力破解
        #map_cp = self.backup()
        from itertools import product
        set_list = []
        for record in record_list:
            set_list.append(record['value_set'])
        record_cp_list = []
        map(record_cp_list.append,record_list)
        #record_cp_list.sort(key=lambda s:s['set_length'])
        #print(record_cp_list)
        map(lambda x:x.pop('value_set'),record_cp_list)
        map(lambda x:x.pop('set_length'),record_cp_list)
        #map(lambda x:x['value'],record_cp_list)

        #print(len(record_cp_list))
        #print(len(set_list))
        for ele_tuple in product(*set_list):
            for i in range(0,len(record_cp_list)):
                record_cp_list[i]['value'] = ele_tuple[i]
                self.map[record_cp_list[i]['i']][record_cp_list[i]['j']] = record_cp_list[i]['value']
            if self.success:
                break
            #print 'failed:',ele_tuple
    '''