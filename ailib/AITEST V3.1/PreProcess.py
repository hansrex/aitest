# -*- coding:utf-8 -*-
# Author: W.S   26/Jan/2018
# A Script to convert from list to relational matrix

import csv
import numpy as np







'''
1   取CSV文件（存储结构待定）
2   读取第一条事件，作为原事件，添加维度#1
3   读取第二条事件，与上一条做比较，不同的话。添加维度#2。【1,2】++1
4   读取第三条事件，与之前所有事件比较，有不同的话，添加维度#3.【2,3】++1
5   读取第四条事件，与之前所有事件比较，有相同的话，此条事件所在维度为curr,上条事件所在维度为last.【last, curr】++
.
.
.
    读取第n条事件，与之前所有事件比较，有相同的话，此条事件所在curr,上条事件（n-1）所在维度为last.【last, curr】++
    
特殊Case：当前读取事件与上条事件相同，如何处理？      这个问题恐怕要单独处理。
                                                    方案#1 合并重复数据。选这个方案！因为矩阵里留有相关的域。例如，【dem_index,dem_index】
                                                    方案#2 剔除重复数据
                                                    
dem_index_list  存储所有事件对应的维度号
matrix_x 矩阵的X轴坐标
matrix_y 矩阵的y轴坐标
def function Check_New_Dem(item)    return TRUE/FALSE
def function Create_New_Dem()       return Dem_index   
def function Find_Spec_Dem(item)    return Dem_index


for item in item_list:
    if check_new( item ):    # 一个检查是否为新item的功能
        Add a new dem      # 添加一个新的维度，有可能需要单独添加一个维度列表
        return a dem index number （Current_Dem_index）# 返回这个维度对应的坐标
    else
        find the spec dem
        return the spec dem index number  (Current_Dem_index)# 返回这个维度对应的坐标
    
    
    check_last_item( item )
        return a dem index number of the last item. (Last_Dem_index) # 返回上一个item所在的维度对应的坐标
    
    matrix_x = Current_Dem_index
    matrix_y = Last_Dem_index
    [ matrix_x, matrix_y ] = ++ 1

处理后的数据两种存储方法：
    1. 把所有东西一直放到矩阵里维护       问题：很难维护
    2. 在每个事件关系（即item到item+1的事件关系）转存起来，后面对应矩阵的坐标，这样就形成一条条记录      主要用这个方案，可以提供一个类似预处理的功能
    
处理前的数据存储方法：
ACTION,OBJECT
left click,Button_1
left click,Button_2
left click,Button_3
left click,Text_Box_1
Type,TestString_1
left click,Button_1
left click,Button_2
left click,Button_3
left click,Text_Box_1
Type,TestString_2
left click,Button_4
left click,Button_6
left click,Button_7
left click,Text_Box_2
Type,TestString_3
left click,Button_8
left click,Button_9
left click,Button_1
left click,Button_2
left click,Button_6
left click,Button_10
left click,Button_11
left click,Text_Box_3
Type,TestString_4
left click,Button_12
'''



# Global Definition
dem_list = [] #item的维度索引表
matrix_x = 0 #事件关系在矩阵里的坐标
matrix_y = 0 #事件关系在矩阵里的坐标
item_list = [] #原始item列表，是一个字符串列表

def read_csv_file():

    with open('D:/1-PROJECTS/Sandbox/tests/DataCollection/raw_dataset.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            item_string = str(row['ACTION']) + ','+ str(row['OBJECT'])
            item_list.append(item_string)
    return item_list

def _get_dem_num(): #查看Dem列表长度
    return len(dem_list)

def _initial_matrix(): #初始化矩阵
    _initial_dem_list()
    max_dem = _get_dem_num()
    matrix_base = np.zeros((max_dem, max_dem))
    return matrix_base

def _initial_dem_list():
    for item in item_list:
        if item not in dem_list:
            dem_list.append(item)




def _check_new_dem(item): #检查该item在维度表里是否是新的事件
    if item in dem_list:
        return 1
    else:
        return 0

def _create_new_dem(item):  #在维度表里添加一个新的事件
    dem_list.append(item)

    new_dem_index = len(dem_list)


    return new_dem_index

def _find_spec_dem(item): #搜索事件在维度表的位置，也就是对应的维度索引号
    spec_dem = 0

    spec_dem = dem_list.index(item)

    return spec_dem

def _check_dem_index(item): #处理单个Item !!!这个需要修改，目前是一次性生成dem_list，后面要琢磨琢磨怎么动态生成dem_list
    if _check_new_dem(item):
        current_dem_index = _find_spec_dem(item) #!!!!TBD!!!!!
    else:
        current_dem_index = _find_spec_dem(item)

    return current_dem_index

def preprocess_matrix(item_list): #处理Item列表

    matrix_base = _initial_matrix()
    current_item = 'null'
    last_item = 'null'

    for item in item_list:
        if current_item == 'null':
            pass
            current_item = item
            last_item = item
        else:
            current_item = item
            current_dem_index = _check_dem_index(current_item)
            last_dem_index = _check_dem_index(last_item)
            matrix_y = current_dem_index
            matrix_x = last_dem_index
            matrix_base[matrix_x,matrix_y] += 1
            last_item = item

    pre_matrix = matrix_base
    return pre_matrix

    '''
    for item in item_list:
        if check_new( item ):    # 一个检查是否为新item的功能
            Add a new dem      # 添加一个新的维度，有可能需要单独添加一个维度列表
            return a dem index number （Current_Dem_index）# 返回这个维度对应的坐标
        else
            find the spec dem
            return the spec dem index number  (Current_Dem_index)# 返回这个维度对应的坐标


        check_last_item( item )
            return a dem index number of the last item. (Last_Dem_index) # 返回上一个item所在的维度对应的坐标

        matrix_x = Current_Dem_index
        matrix_y = Last_Dem_index
        [ matrix_x, matrix_y ] = ++ 1

    两种存储方法：
        1. 把所有东西一直放到矩阵里维护       问题：很难维护
        2. 在每个事件关系（即item到item+1的事件关系）转存起来，后面对应矩阵的坐标，这样就形成一条条记录      主要用这个方案，可以提供一个类似预处理的功能

    '''

if __name__ == '__main__':
    item_list = read_csv_file()
    MAT = preprocess_matrix(item_list)
    print MAT

    AR = np.asarray(MAT)
    print AR
    print type(AR)

    for item in dem_list:
        print item

    # Post_MAT = maximum_spanning_arborescence_V1(MAT)

