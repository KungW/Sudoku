#coding:utf-8
__author__ = 'Tony Lu'

from SudokuParser import SudokuParser
from SudokuSpider import SudokuSpider

def read_saved_maps_by_file(map_data_set_file):
    #读取保存在txt中的地图
    return SudokuSpider(need_web=False).get_map_list_by_read(map_data_set_file)

def read_saved_maps_by_database(grade=None):
    return SudokuSpider(need_web=False).get_map_list_by_database(grade=grade)


def save_maps_by_file(map_list,map_data_set_file):
    '''将地图集保存到某文件中'''
    try:
        for map in map_list:
            data_str = SudokuSpider(need_web=False).map_dict_to_str(map)
            print(data_str)
            map_data_set_file.write(data_str+'\n')
        return True
    except Exception as e:
        print('save_maps():'+str(e))
    return False

def parse_maps(map_list):
    '''
        解析地图集，计算成功率
        生成并返回其中的无解、多解地图集，
    '''
    success_cot = 0
    #err_map_list = []
    multi_answer_map_list = []
    for map in map_list:
        sudoku = SudokuParser(map)
        back_up = sudoku.backup(map)
        sudoku.parse()
        sudoku.show_result()
        if sudoku.answer_length==1:
            success_cot += 1
        elif sudoku.answer_length==0:
            #print('origin_map')
            #sudoku.show(extend_map=back_up)
            #print('current_map')
            #sudoku.show()
            #err_map_list.append(back_up)
            pass
        else:
            multi_answer_map_list.append(map)
    success_rate = success_cot * 1.0 / len(map_list)
    print('success:{}  total:{}  rate:{}%'.format(success_cot,len(map_list),success_rate*100))
    return {
        'success_cot':          success_cot,
        'total_cot':            len(map_list),
        'success_rate':         success_rate,
        #'err_map_list':         err_map_list,
        #'multi_answer_map_list':multi_answer_map_list,
    }


def main_test(
        map_list,
        need_save_multi_answer_map_set=False,
        multi_answer_map_set_file=None,
        need_save_error_map_set=False,
        error_map_set_file=None
              ):

    '''主测试'''
    result_dict = parse_maps(map_list)

    err_map_list = []
    multi_answer_map_list=[]

    #err_map_list = result_dict['err_map_list']
    #multi_answer_map_list = result_dict['multi_answer_map_list']

    if need_save_error_map_set:
        if not error_map_set_file:
            error_map_set_file = file('maps/err_map_set.txt','a')
        #保存错误数据
        if save_maps_by_file(
            map_list = err_map_list,
            map_data_set_file = error_map_set_file
        ):
            print('save error_map set success')

    if need_save_multi_answer_map_set:
        if not multi_answer_map_set_file:
            multi_answer_map_set_file = file('maps/multi_answer_map_set.txt','a')
        #保存多解地图数据
        if save_maps_by_file(
            map_list = multi_answer_map_list,
            map_data_set_file = multi_answer_map_set_file
        ):
            print('save multi_answer_map set success')

    return result_dict