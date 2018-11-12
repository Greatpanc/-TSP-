# -*- coding: utf-8 -*-
"""
	基于分支限定法的旅行商问题解法Python源码
	
	Author:	Greatpan
	Date:	2018.10.3
"""

import time
import math
from queue import Queue
from MyFuncTool import GetData,ResultShow,draw,Node


def create_node(cur_node,next_city):
	"""
		函数名：create_node(cur_node,next_city)
		函数功能：	根据当前的点构建走向下一个城市的点信息
			输入	1 	cur_node：从出发点到当前城市节点信息
				2	next_city：下一个城市
			输出	1	next_node:表示从出发点到当前城市下一个城市的节点信息
		其他说明：无
	"""
	next_node=Node(CityNum)
	next_node.start=cur_node.start 		#沿着cur_node走到next，起点不变 
	next_node.pathsum=cur_node.pathsum+Dist[cur_node.end][next_city]
	next_node.end=next_city 			#更新最后一个点
	next_node.num=cur_node.num+1
	next_node.listc=cur_node.listc.copy()
	next_node.listc.append(next_city)
	next_node.visited=cur_node.visited.copy()
	next_node.visited[next_city] = True

	return next_node


def BaBMethod(CityNum,Dist):
	"""
		函数名：BaBMethod(CityNum,Dist)
		函数功能：	分支限定算法核心
			输入	1 	CityNum：城市数量
				2	Dist：城市间距离矩阵
			输出	1 Min_Path：最优路径长
				2 cur_node：最优路径
		其他说明：无
	"""

	node=Node(CityNum)	#出发城市的节点信息
	node.end=0 			#结束点到0结束(当前路径的结束点)
	node.num+=1 		#遍历过得点数，初始1个
	node.listc.append(0)
	node.visited[0]=True

	Min_Path=math.inf 	#Min_Path是问题的最终解
	pri_queue = Queue() #创建一个队列
	pri_queue.put(node) #将起点加入队列
	while pri_queue.qsize()!=0: 
		cur_node=pri_queue.get()
		#如果所有城市都遍历完成，则记录最小
		if cur_node.num==CityNum:
			ans=cur_node.pathsum+Dist[cur_node.start][cur_node.end]	 	#总的路径消耗
			if(Min_Path>ans):
				Min_Path=ans
				BestPath=cur_node.listc.copy()

		#当前点可以向下扩展的点加入队列中
		for i in range(CityNum):
			if cur_node.visited[i]==False:
				next_node=create_node(cur_node,i)
				pri_queue.put(next_node)
	BestPath.append(0)
	return Min_Path,BestPath

##############################程序入口#########################################
if __name__ == "__main__":
	Position,CityNum,Dist = GetData("./data/TSP10cities.tsp")

	start = time.clock()				#程序计时开始
	Min_Path,BestPath=BaBMethod(CityNum,Dist)	#调用分支限定法
	end = time.clock()					#程序计时结束

	print()
	ResultShow(Min_Path,BestPath,CityNum,"穷举法的宽度优先搜索策略")
	print("程序的运行时间是：%s"%(end-start))
	draw(BestPath,Position,"Breadth First Search Method")
"""
结果：
基于穷举法的宽度优先搜索策略求得最短旅行商经过所有城市回到原城市的最短路径为：
0->4->6->7->1->3->2->5->8->9->0
总路径长为：10127.552143541276

程序的运行时间是：12.336137899
"""

