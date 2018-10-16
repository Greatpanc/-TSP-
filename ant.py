# -*- coding: utf-8 -*-
"""
	基于回溯法的旅行商问题解法Python源码

	Author:	Greatpan
	Date:	2018.10.10
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import time
from MyFuncTool import *

"""
	函数名：ant()
	函数功能：蚁群算法核心
		输入	1: 无
		输出	1: 无
	其他说明：无
"""
def ant():
    numant = 5          #蚂蚁个数
    numcity = CityNum   #城市个数
    alpha = 1           #信息素重要程度因子
    beta = 5            #启发函数重要程度因子
    rho = 0.1           #信息素的挥发速度
    Q = 1

    iter = 0
    itermax = 50

    etatable = 1.0/(Dist+np.diag([1e10]*numcity)) #启发函数矩阵，表示蚂蚁从城市i转移到矩阵j的期望程度
    pheromonetable  = np.ones((numcity,numcity)) # 信息素矩阵
    pathtable = np.zeros((numant,numcity)).astype(int) #路径记录表


    lengthaver = np.zeros(itermax) #各代路径的平均长度
    lengthbest = np.zeros(itermax) #各代及其之前遇到的最佳路径长度
    pathbest = np.zeros((itermax,numcity)) # 各代及其之前遇到的最佳路径长度


    while iter < itermax:


        # 随机产生各个蚂蚁的起点城市
        if numant <= numcity:#城市数比蚂蚁数多
            pathtable[:,0] = np.random.permutation(range(0,numcity))[:numant]
        else: #蚂蚁数比城市数多，需要补足
            pathtable[:numcity,0] = np.random.permutation(range(0,numcity))[:]
            pathtable[numcity:,0] = np.random.permutation(range(0,numcity))[:numant-numcity]

        length = np.zeros(numant) #计算各个蚂蚁的路径距离

        for i in range(numant):


            visiting = pathtable[i,0] # 当前所在的城市

            #visited = set() #已访问过的城市，防止重复
            #visited.add(visiting) #增加元素
            unvisited = set(range(numcity))#未访问的城市
            unvisited.remove(visiting) #删除元素


            for j in range(1,numcity):#循环numcity-1次，访问剩余的numcity-1个城市

                #每次用轮盘法选择下一个要访问的城市
                listunvisited = list(unvisited)

                probtrans = np.zeros(len(listunvisited))

                for k in range(len(listunvisited)):
                    probtrans[k] = np.power(pheromonetable[visiting][listunvisited[k]],alpha)\
                            *np.power(etatable[visiting][listunvisited[k]],alpha)
                cumsumprobtrans = (probtrans/sum(probtrans)).cumsum()

                cumsumprobtrans -= np.random.rand()

                k = listunvisited[np.where(cumsumprobtrans>0)[0][0]] #下一个要访问的城市

                pathtable[i,j] = k

                unvisited.remove(k)
                #visited.add(k)

                length[i] += Dist[visiting][k]

                visiting = k

            length[i] += Dist[visiting][pathtable[i,0]] #蚂蚁的路径距离包括最后一个城市和第一个城市的距离


        #print length
        # 包含所有蚂蚁的一个迭代结束后，统计本次迭代的若干统计参数

        lengthaver[iter] = length.mean()

        if iter == 0:
            lengthbest[iter] = length.min()
            pathbest[iter] = pathtable[length.argmin()].copy()      
        else:
            if length.min() > lengthbest[iter-1]:
                lengthbest[iter] = lengthbest[iter-1]
                pathbest[iter] = pathbest[iter-1].copy()

            else:
                lengthbest[iter] = length.min()
                pathbest[iter] = pathtable[length.argmin()].copy()    


        # 更新信息素
        changepheromonetable = np.zeros((numcity,numcity))
        for i in range(numant):
            for j in range(numcity-1):
                changepheromonetable[pathtable[i,j]][pathtable[i,j+1]] += Q/Dist[pathtable[i,j]][pathtable[i,j+1]]

            changepheromonetable[pathtable[i,j+1]][pathtable[i,0]] += Q/Dist[pathtable[i,j+1]][pathtable[i,0]]
        pheromonetable = (1-rho)*pheromonetable + changepheromonetable

        iter += 1 #迭代次数指示器+1

    path_tmp=pathbest[-1]
    BestPath=[]
    for i in path_tmp:
        BestPath.append(int(i))
    BestPath.append(BestPath[0])

    return BestPath,lengthbest[-1]

##############################程序入口#########################################
if __name__ == "__main__":
    Position,CityNum,Dist = GetData("./data/TSP100cities.tsp")

    start = time.clock()				#程序计时开始
    BestPath,Min_Path = ant()
    end = time.clock()					#程序计时结束

    print()
    ResultShow(Min_Path,BestPath,CityNum,"蚁群算法")
    draw(BestPath,Position,"Ant Method")

