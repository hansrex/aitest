# -*- coding:utf-8 -*-


from sklearn.cluster import DBSCAN
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

#---------------------------------------读CSV文件----------------------------------------
X_Column = []
Y_Column = []
with open('DB.csv') as csvfile:
     reader = csv.DictReader(csvfile)
     for row in reader:
        X_Column.append(float(row['POS_X']))
        Y_Column.append(float(row['POS_Y']))
fig, ax = plt.subplots() #这句是硬copy的，To be updated
x = np.array(X_Column) #太多x,y之类的命名，TBD
y = np.array(Y_Column)


#---------------------------------------画散点图----------------------------------------
colors = ['k']*len(x)
ax.scatter(x, y, c=colors, alpha=0.5) #散点图


#---------------------------------------调整坐标系格式，添加辅助图形----------------------------------------
plt.plot(x,y)
# plt.plot([500, 1000], [0, 1500])
ax.add_patch(patches.Rectangle((0,0),1920,1080,fill=False,alpha = 0.3)) #显示分辨率
ax.set_xlim((0,2000))
ax.set_ylim((0,2000))
x0,x1 = ax.get_xlim()
y0,y1 = ax.get_ylim()
ax.set_aspect(abs(x1-x0)/abs(y1-y0))
ax.grid(b=True, which='major', color='k', linestyle='--')

major_ticks = np.arange(0, 2001, 500) #用2001,而不是2000，否则显示不出2000
minor_ticks = np.arange(0, 2001, 100)

ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor=True)
ax.set_yticks(major_ticks)
ax.set_yticks(minor_ticks, minor=True)

ax.grid(which='both')

ax.grid(which='minor', alpha=0.2)
ax.grid(which='major', alpha=0.5)


X =np.column_stack((x,y)) #用List X,Y生成矩阵
# pca =PCA(n_components=2)
# pca.fit(X)
#
#
# fig = plt.figure(1)
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(X[:, 0], X[:, 1])

# X_new = pca.transform(X)

X_new = X #目前X_new和X没有区别，后面要加X的一个预处理，产生X_new

##设置分层聚类函数
db = DBSCAN(eps=50, min_samples=2) #最小核心样本为2，
##训练数据
db.fit(X_new)
##初始化一个全是False的bool类型的数组
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
'''
   这里是关键点(针对这行代码：xy = X[class_member_mask & ~core_samples_mask])：
   db.core_sample_indices_  表示的是某个点在寻找核心点集合的过程中暂时被标为噪声点的点(即周围点
   小于min_samples)，并不是最终的噪声点。在对核心点进行联通的过程中，这部分点会被进行重新归类(即标签
   并不会是表示噪声点的-1)，也可也这样理解，这些点不适合做核心点，但是会被包含在某个核心点的范围之内
'''
core_samples_mask[db.core_sample_indices_] = True

##每个数据的分类
lables = db.labels_






##分类个数：lables中包含-1，表示噪声点
n_clusters_ = len(np.unique(lables)) - (1 if -1 in lables else 0)

##绘图
unique_labels = set(lables)
'''
   1)np.linspace 返回[0,1]之间的len(unique_labels) 个数
   2)plt.cm 一个颜色映射模块
   3)生成的每个colors包含4个值，分别是rgba
   4)其实这行代码的意思就是生成4个可以和光谱对应的颜色值
'''

########################################################从lables生成邻接矩阵

dem = len(unique_labels) - 1
M1 = np.zeros((dem, dem))
lables_len = len(lables)
processed_lables = []

for i in range(0,lables_len):
    if lables[i] == -1:
        pass
    else:
        processed_lables.append(lables[i])
print(lables)
print(processed_lables)

for i in range(0,len(processed_lables)):
    print (i+1)
    print len(processed_lables)
    if i+1 < len(processed_lables):
        if processed_lables[i+1] == processed_lables[i]:
            pass
        else:
            x_add = processed_lables[i]
            y_add = processed_lables[i+1]
            M1[x_add,y_add] = M1[x_add,y_add] + 1
print(M1)
########################################################从lables生成邻接矩阵

########################################################只针对无向图的矩阵转换

for i in range(0,dem):
    for j in range(0,dem):
        if M1[i,j] <> 0 and M1[j,i] <> 0:
            M1[i,j] = M1[i,j] + M1[j,i]
            M1[j,i] = 0

print(M1)

########################################################只针对无向图的矩阵转换





colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))

# plt.subplot(2)
plt.figure(2)
plt.clf()

ax = plt.gca()
ax.set_xlim((0,2000))
ax.set_ylim((0,2000))
ax.add_patch(patches.Rectangle((0,0),1920,1080,fill=False,alpha = 0.3))


x0,x1 = ax.get_xlim()
y0,y1 = ax.get_ylim()
ax.set_aspect(abs(x1-x0)/abs(y1-y0))
ax.grid(b=True, which='major', color='k', linestyle='--')

# major ticks every 20, minor ticks every 5
major_ticks = np.arange(0, 2001, 500)
minor_ticks = np.arange(0, 2001, 100)

ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor=True)
ax.set_yticks(major_ticks)
ax.set_yticks(minor_ticks, minor=True)

# and a corresponding grid

ax.grid(which='both')

# or if you want differnet settings for the grids:
ax.grid(which='minor', alpha=0.2)
ax.grid(which='major', alpha=0.5)

plt.plot(x,y)

Cluster_X = []
Cluster_Y = []
Cluster_NO = []

for k, col in zip(unique_labels, colors):
    ##-1表示噪声点,这里的k表示黑色
    if k == -1:
        col = 'k'

    ##生成一个True、False数组，lables == k 的设置成True
    class_member_mask = (lables == k)

    ##两个数组做&运算，找出即是核心点又等于分类k的值  markeredgecolor='k',
    xy = X_new[class_member_mask & core_samples_mask]
    # plt.plot(xy[:, 0], xy[:, 1], 'o', c=col, markersize=6)
    plt.plot(xy[:, 0], xy[:, 1], 'o', c=col, markersize=6,alpha = 0.5)
    plt.plot(float(np.mean(xy[:, 0])),float(np.mean(xy[:, 1])),'o', c=col, markersize=16, alpha = 0.2) #抽象为几个点
    Cluster_X.append(float(np.mean(xy[:, 0])))
    Cluster_Y.append(float(np.mean(xy[:, 1])))
    # plt.plot(xy[:, 0], xy[:, 1])
    '''
       1)~优先级最高，按位对core_samples_mask 求反，求出的是噪音点的位置
       2)& 于运算之后，求出虽然刚开始是噪音点的位置，但是重新归类却属于k的点
       3)对核心分类之后进行的扩展
    '''
    xy = X_new[class_member_mask & ~core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', c=col, markersize=6, alpha = 0.5) #噪声点
    # plt.plot(xy[:, 0], xy[:, 1], 'o', c=col, markersize=6)




plt.title('Estimated number of operation clusters: %d' % n_clusters_)



plt.figure(3)

ax = plt.gca()
ax.set_xlim((0,2000))
ax.set_ylim((0,2000))
ax.add_patch(patches.Rectangle((0,0),1920,1080,fill=False,alpha = 0.3))


x0,x1 = ax.get_xlim()
y0,y1 = ax.get_ylim()
ax.set_aspect(abs(x1-x0)/abs(y1-y0))
ax.grid(b=True, which='major', color='k', linestyle='--')

# major ticks every 20, minor ticks every 5
major_ticks = np.arange(0, 2001, 500)
minor_ticks = np.arange(0, 2001, 100)

ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor=True)
ax.set_yticks(major_ticks)
ax.set_yticks(minor_ticks, minor=True)

# and a corresponding grid

ax.grid(which='both')

# or if you want differnet settings for the grids:
ax.grid(which='minor', alpha=0.2)
ax.grid(which='major', alpha=0.5)
Cluster_x = np.array(Cluster_X)
Cluster_y = np.array(Cluster_Y)


# plt.plot(Cluster_x,Cluster_y)
# plt.arrow(0,0,100,100,head_width = 1)
for i in range(0,dem):
    for j in range(0,dem):
        print('Metrix M1[i,j]:'),
        print  M1[i,j]
        if M1[i,j] <> 0:
            print ('A Line to be printed!!!')
            print (Cluster_x[i],Cluster_x[j],Cluster_x[i],Cluster_y[j])
            plt.plot([Cluster_x[i],Cluster_x[j]],[Cluster_y[i],Cluster_y[j]],linewidth = M1[i,j]*3,alpha = 0.5)

plt.plot(Cluster_x,Cluster_y,'o', c=col, markersize=16,alpha = 0.3)
# plt.plot([1208.25, 959.0], [1208.25, 733.0])
plt.show()