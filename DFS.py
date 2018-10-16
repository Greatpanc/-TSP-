# -*- coding: utf-8 -*-
"""
	基于深度优先搜索（穷举法）的旅行商问题解法Python源码

	Author:	Greatpan
	Date:	2018.10.10
"""
import pandas as pd
import numpy as np
import math
import time
from MyFuncTool import *

"""
	函数名：CalcPath_sum(layer,i)
	函数功能：计算从初始城市到第layer层再到接下来的第i个城市所经历的总距离
		输入	1: layer 回溯所处的层数，也即所遍历的城市数
			2: i 当前层数下接下来要访问的子节点，即要访问的下一个城市
		输出	1: Path_sum 求的的是当前递归所处的层数的累积路径值+到下一个节点的距离
	其他说明：无
"""
def CalcPath_sum(layer,i):
    #计算从初始城市到第layer层
    Path_sum = sum([Dist[city1][city2] for city1,city2 in zip(Curpath[:layer], Curpath[1:layer+1])])
    
    #计算从初始城市到第layer层再到接下来的第i个城市所经历的总距离
    Path_sum += Dist[Curpath[i-1]][i]

    return Path_sum

"""
	函数名：DFSMethod(Dist,CityNum,layer)
	函数功能： 深度优先搜索算法核心
		输入	1 CityNum：城市数量
			2 Dist：城市间距离矩阵
            3 layer:旅行商所处层数，也即遍历的城市数
		输出	：无
	其他说明：无
"""
def DFSMethod(Dist,CityNum,layer):
    global Path_sum,Cur_Min_Path,Min_Path,BestPath
    #如果所有城市都遍历完成，则记录最小
    if(layer==CityNum):
        Path_sum=CalcPath_sum(layer,0)
        if(Path_sum<=Cur_Min_Path):
            Cur_Min_Path=Path_sum
            Min_Path=Cur_Min_Path
            BestPath=Curpath.tolist()
            BestPath.append(0)
    #否则递归回溯
    else:
        for i in range(layer,CityNum):
            Curpath[i],Curpath[layer] = Curpath[layer],Curpath[i]  # 路径交换一下
            DFSMethod(Dist, CityNum, layer+1)
            Curpath[i],Curpath[layer] = Curpath[layer],Curpath[i]  # 路径交换回来

##############################程序入口#########################################
if __name__ == "__main__":
    Position,CityNum,Dist = GetData("./data/TSP10cities.tsp")
    Curpath = np.arange(CityNum)
    Min_Path=0
    BestPath=[]
    Cur_Min_Path = math.inf

    start = time.clock()				#程序计时开始
    DFSMethod(Dist,CityNum,1)	        #调用深度优先搜索核心算法
    end = time.clock()					#程序计时结束

    print()
    ResultShow(Min_Path,BestPath,CityNum,"穷举法之深度优先搜索策略")
    print("程序的运行时间是：%s"%(end-start))
    draw(BestPath,Position,"DFS Method")

"""
结果：
穷举法之深度优先搜索策略求得最短旅行商经过所有城市回到原城市的最短路径为：
0->4->6->7->1->3->2->5->8->9->0
总路径长为：10127.552143541276

程序的运行时间是：4.845021001
"""

