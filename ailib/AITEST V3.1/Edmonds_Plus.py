# -*- coding:utf-8 -*-
# Author: W.S   16/Dec/2017
# A Script to deal with tree graphic

'''
主要使用了Edmonds算法（朱刘算法）。
这里处理的数据是PreProcess预处理的数据，并不是原始数据。
Edmonds目前不支持自定义根节点。方案1:更新算法（太难！）    方案2：修剪关系矩阵（有点Low,但是可以实现目标） TBD！！！！
Pre_Process.dem_list未来会成为预处理后的数据库，目前暂时存在内存里。另外说一点，对于稀疏矩阵的存储，主要有三种方式：
1.横表（易于理解和计算，其实就是把关系矩阵直接存数据库里了，但是不易维护）
2.纵表（类似于一个关系表，子节点，父节点之类的。不太好理解和计算，据说利于维护TBC）
3.三元组（吼吼吼吼，我的发明。。。才怪。一直这种方式，比较方便理解，便于计算和维护） 目前dem_list会以三元组的方式保存

G是图（有向树形图）
T是树（有向树）
Z是测试用的矩阵，to be deleted!!!


******************************待解决问题**************************************
（Done)1. 作为demo演示的话，显示效果太。。。。丑。。。。，图像显示要单独准备一下。（Done,调整了一下显示效果，并提供了多个配色方案 ^0^开心）
2. 路是走通了，但是对于原始数据（也就是action list)的预处理，还是要再专业点。如type test和click button往往是成对出现的，
这里需要预处理的。此类问题要多想想。
3. 预处理产生的关系矩阵的存储。
4. 例如Action.A -> Action.A -> Action.A这种事件关系会存储在关系矩阵中（Pre_MAT),但是目前还没有逻辑或算法去挖掘这部分
数据的价值，这个后面要考虑一下。
5. 对于RDF标准，后面可以考虑应用到整个方案中。RDF在互联网圈应该是个趋势。实用性和通用性有待考察。
6. PreProcess目前是一次性生成dem_list,后面要加上动态生成方法。

'''
from __future__ import division
import matplotlib.pyplot as plt
import networkx as nx
import networkx.readwrite as rd
import json
import JsonParser



import networkx.algorithms.tree.branchings  as brch
import PreProcess

def maximum_spanning_arborescence_V1(G, attr='weight', default=0): #改写了一下maximum_spanning_arborescense
    ed = brch.Edmonds(G)
    Post_G = ed.find_optimum(attr, default, kind='max', style='arborescence')
    return Post_G


def Process():
    PreProcess.item_list = PreProcess.read_csv_file() #读csv数据
    Pre_MAT = PreProcess.preprocess_matrix(PreProcess.item_list) #预处理数据，生成Pre_MAT关系矩阵

    G = nx.from_numpy_matrix(Pre_MAT, create_using=nx.MultiDiGraph()) #G多重加权有向图
    T = maximum_spanning_arborescence_V1(G) #利用改写的朱刘算法，生成最小树形图T
    return G,T

def ToJson():
    G,T = Process()
    # labels = {i: '<' + str(i) + '>' + PreProcess.dem_list[i] for i in G.nodes()}
    # T.node[1]['label'] = 'teststring'
    for i in G.nodes():
        G.node[i]['label_test'] = PreProcess.dem_list[i]
    # data = rd.json_graph.node_link_data(T)
    data = JsonParser.node_link_data(G)
    _ToJsonFile(data)
    S = json.dumps(data)
    print S

def _preprocess_Json(G,labels):
    pos = nx.circular_layout(G)
    _preprocess_Json_nodes = nx.draw_networkx_labels(G, pos, labels, font_size=10, alpha= 0.7)

    return _preprocess_Json_nodes

def _ToJsonFile(data):
    with open("write.json", "w") as f:
        json.dump(data, f, indent=4, sort_keys=True)

def _color_style(selection):

    edge_style = '#000000'
    node_style = '#000000'
    node_font_style = '#000000'
    edge_font_style = '#000000'
    BG_style = '#000000'

    if selection == 0: # 海洋风格
        edge_style = '#003B46'
        node_style = '#66A5AD'
        node_font_style = '#07575B'
        edge_font_style = '#07575B'
        BG_style = '#C4DFE6'

    elif selection == 1: # 醒目风格
        edge_style = '#063852'
        node_style = '#F0810F'
        node_font_style = '#011A27'
        edge_font_style = '#011A27'
        BG_style = '#E6DF44'

    elif selection == 2: #很土的风格
        edge_style = '#258039'
        node_style = '#CF3721'
        node_font_style = '#F5BE41'
        edge_font_style = '#F5BE41'
        BG_style = '#31A9B8'

    elif selection == 3: #清爽菜园的风格
        edge_style = '#739F3D'
        node_style = '#F69454'
        node_font_style = '#EE693F'
        edge_font_style = '#EE693F'
        BG_style = '#FCFDFE'

    elif selection == 4: #清爽菜园的风格+
        edge_style = '#F69454'
        node_style = '#739F3D'
        node_font_style = '#EE693F'
        edge_font_style = '#EE693F'
        BG_style = '#FCFDFE'

    elif selection == 5: #专业风格
        edge_style = '#1E1E20'
        node_style = '#BBC3C6'
        node_font_style = '#962715'
        edge_font_style = '#962715'
        BG_style = '#FFFFFF'

    elif selection == 6: #城市风格
        edge_style = '#DDDEDE'
        node_style = '#A5C05B'
        node_font_style = '#232122'
        edge_font_style = '#232122'
        BG_style = '#7BA4A8'

    elif selection == 7: #少女风
        edge_style = '#FCFCFA'
        node_style = '#337BAE'
        node_font_style = '#FFBEBD'
        edge_font_style = '#FFBEBD'
        BG_style = '#1A405F'

    elif selection == 8: #现代风格+
        edge_style = '#3A5199'
        node_style = '#D5D6D2'
        node_font_style = '#2F2E33'
        edge_font_style = '#2F2E33'
        BG_style = '#FFFFFF'

    else:
        pass

    return edge_style, node_style, node_font_style, edge_font_style, BG_style


def _layout(pos_case,G): #layout选择功能
    if pos_case == 0:
        pos = nx.circular_layout(G)
        print('Circular')
    elif pos_case == 1:
        pos = nx.kamada_kawai_layout(G)
        print('Kamada_Kawai')
    elif pos_case == 2:
        pos = nx.random_layout(G)
        print('Random')
    elif pos_case == 3:
        pos = nx.rescale_layout(G)
        print('Rescale')
    elif pos_case == 4:
        pos = nx.shell_layout(G)
        print('Shell')
    elif pos_case == 5:
        pos = nx.spectral_layout(G)
        print('Spectral')
    elif pos_case == 100:
        pos = nx.nx_agraph.graphviz_layout(G, prog = 'neato', root= 3)
        print('Graphviz')
    elif pos_case == 101:
        pos = nx.spring_layout(G)
        print('Spring Layout')
    else:
        pos = nx.spring_layout(G, k=5, iterations= 35)
        print('Other Choice')
    return pos

def _toGraph(G,
             _figure_name,
             pos,
             labels,
             edge_labels,
             node_sizes,_has_root):

    edge_style, node_style, node_font_style, edge_font_style, BG_style = _color_style(4)


    fig = plt.figure(_figure_name)
    M = G.number_of_edges()
    N = G.number_of_nodes()
    weights = [d['weight']*1.5 for u, v, d in G.edges(data=True)]
    max_weight = max(weights)

    nx.draw_networkx_labels(G, pos, labels, font_size=10, font_color= node_font_style, alpha= 0.7)
    nx.draw_networkx_nodes(G, pos, node_size= 500, node_color=node_style, alpha=0.8)

    edges = nx.draw_networkx_edges(G, pos, node_size=node_sizes, arrowstyle='-|>', arrowsize=25, edge_color=edge_style, width= 3, alpha= 0.3)
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, alpha=0.8, font_color = edge_font_style)

    for i in range(M):
        if weights[i]< max_weight*0.3:
            edges[i].set_alpha(0.3)
        else:
            edges[i].set_alpha((weights[i])/(max_weight*1))

    if _has_root == 1: # 对于MAT图，标记根节点
        root_set = {n for n, d in G.in_degree() if d == 0}
        root_num = root_set.pop()
        nx.draw_networkx_nodes(G, pos, nodelist=[root_num], node_shape='s', node_size=2000, node_color= node_font_style, alpha= 0.4)

    fig.set_facecolor(BG_style)
    plt.axis('off')
    plt.show()

def To_DiGraph():

    G,T = Process()

    pos_case =-1 # 可选项，后面改成入参
    print pos_case
    pos = _layout(pos_case,G)

    labels = {i : '<'+ str(i) +'>'+ PreProcess.dem_list[i] for i in G.nodes()} #这里的labels是Node labels，至于格式，后面可以规范一下。TBD
    edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)} #这回去edge的labels,取值用weight。后面希望能根据weight更改edge的显示效果

    # *****************************测试代码**********************************
    edge_weight_list =  edge_labels.values()

    edge_alphas = edge_weight_list
    for i in range(0,len(edge_weight_list)-1):
        wt = int(edge_weight_list[i])
        edge_alphas[i] = (3 - wt)/3
    # *****************************测试代码**********************************


    node_sizes = [3 + 10 * i for i in range(len(G))] #目前点的大小是渐变的

    _toGraph(G,'RAW',pos,labels,edge_labels,node_sizes,0)




    pos = _layout(pos_case,T)
    labels = {i: '<' + str(i) + '>' + PreProcess.dem_list[i] for i in
              T.nodes()}  # 这里的labels是Node labels，至于格式，后面可以规范一下。TBD
    edge_labels = {(u, v): d['weight'] for u, v, d in
                   T.edges(data=True)}  # 这回去edge的labels,取值用weight。后面希望能根据weight更改edge的显示效果

    _toGraph(T,'MAT', pos, labels, edge_labels, node_sizes,1)


    P = nx.dfs_preorder_nodes(T)
    print list(P)



if __name__ == '__main__':
    # To_DiGraph()
    ToJson()