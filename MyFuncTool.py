# -*- coding: utf-8 -*-
"""
	基于贪心算法的旅行商问题解法Python源码
	
	Author:	Greatpan
	Date:	2018.9.30
"""
import pandas
import numpy as np
import math
import matplotlib.pyplot as plt 
import time

class Node:
    def __init__(self,CityNum):
        self.visited=[False]*CityNum    #记录城市是否走过
        self.start=0                    #起点城市
        self.end=0                      #目标城市
        self.current=0                  #当前所处城市
        self.num=0                      #走过的城市数量
        self.pathsum=0                  #走过的总路程
        self.lb=0                       #当前结点的下界
        self.listc=[]                   #记录依次走过的城市

"""
	函数名：GetData()
	函数功能：	从外界读取城市数据并处理
		输入	无
		输出	1 Position：各个城市的位置矩阵
			2 CityNum：城市数量
			3 Dist：城市间距离矩阵
	其他说明：无
"""
def GetData(datapath):
	dataframe = pandas.read_csv(datapath,sep=" ",header=None)
	Cities = dataframe.iloc[:,1:3]
	Position= np.array(Cities)				#从城市A到B的距离矩阵
	CityNum=Position.shape[0]				#CityNum:代表城市数量
	Dist = np.zeros((CityNum,CityNum))		#Dist(i,j)：城市i与城市j间的距离

	#计算距离矩阵
	for i in range(CityNum):
		for j in range(CityNum):
			if i==j:
				Dist[i,j] = math.inf
			else:
				Dist[i,j] = math.sqrt(np.sum((Position[i,:]-Position[j,:])**2))
	return Position,CityNum,Dist

def ResultShow(Min_Path,BestPath,CityNum,string):
    print("基于"+string+"求得的旅行商最短路径为：")
    for m in range(CityNum):
        print(str(BestPath[m])+"—>",end="")
    print(BestPath[CityNum])
    print("总路径长为："+str(Min_Path))
    print()

"""
	函数名：draw(BestPath,Position,title)
	函数功能：	通过最优路径将旅行商依次经过的城市在图表上绘制出来
		输入	1 	BestPath：最优路径
			2	Position：各个城市的位置矩阵
			3	title:图表的标题
		输出	无
	其他说明：无
"""
def draw(BestPath,Position,title):
	plt.title(title) 
	plt.plot(Position[:,0],Position[:,1],'bo')
	for i,city in enumerate(Position): 
		plt.text(city[0], city[1], str(i)) 
	plt.plot(Position[BestPath, 0], Position[BestPath, 1], color='red') 
	plt.show()
