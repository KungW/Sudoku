#coding:utf-8

__author__ = 'Lyn  <tonylu716@gmail.com>'
from func import *

if __name__=="__main__":

    '''
    map_list = read_saved_maps_by_file(
        map_data_set_file = file('maps/map_data_set.txt','r')
    )
    '''

    result_dict_list = []
    for i in range(5):
        map_list = read_saved_maps_by_database(grade=i)
        result_dict = main_test(map_list)
        result_dict_list.append(result_dict)


    print('\n\n----------Summary-----------------')
    for result_dict in result_dict_list:
        print(result_dict)