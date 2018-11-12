# -*- coding: utf-8 -*-
"""
	基于分支限定法的旅行商问题解法Python源码
	
	Author:	Greatpan
	Date:	2018.10.3
"""

import math
import time
from queue import Queue
import Greedy
from MyFuncTool import GetData,ResultShow,draw,Node


def get_up(CityNum,Dist):
	"""
		函数名：get_up(CityNum,Dist)
		函数功能：	通过贪心算法求取目标函数的上界
			输入	1 	CityNum：城市数量
				2	Dist：城市间距离矩阵
			输出	1 Path_Up：分支界限法的上界
		其他说明：无
	"""
	Path_Up=Greedy.GreedyMethond(CityNum,Dist)[0]
	return Path_Up


def get_lb(node):
	"""
		函数名：get_lb(node)
		函数功能：	获取旅行商在走到node（城市）点时，到走完全程最小路程
			输入	1 	node：Node类结构数据，node点记录了旅行商走过城市的路径，
				以及还未遍历的城市的信息。
			输出	1	Min_Path:表示旅行商处于node时，接下来要走完全程不可能低于的
				路程值，即node点的下界。
		其他说明：无
	"""
	Min_Path=node.pathsum*2
	#从起点到未遍历城市中的最近一个城市的距离
	min1=math.inf
	for i in range(CityNum):
		if node.visited[i]==False and min1>Dist[i][node.start]:
			min1=Dist[i][node.start]
	Min_Path=Min_Path+min1 if min1!=math.inf else Min_Path

	#从终点到未遍历城市中的最近一个城市的距离
	min2=math.inf
	for i in range(CityNum):
		if node.visited[i]==False and min2>Dist[node.end][i]:
			min2=Dist[node.end][i]
	Min_Path=Min_Path+min2 if min2!=math.inf else Min_Path

	#求所有未遍历的城市，去和离开的两个最小距离
	for i in range(CityNum):
		if node.visited[i]==False:
			min1=min2=math.inf
			#该循环主要是找到去第i个未遍历的城市的最小距离 
			for j in range(CityNum):	
				if min1 > Dist[i][j]:
					min1=Dist[i][j]
					temp=j
			#该循环主要是从第i个未遍历的城市离开的最小距离
			for k in range(CityNum):
				if min2 > Dist[k][i] and k!=temp:
					min2=Dist[i][k]
			Min_Path=Min_Path+min1 if min1!=math.inf else Min_Path
			Min_Path=Min_Path+min2 if min2!=math.inf else Min_Path
	return Min_Path/2


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
	next_node.pathsum=cur_node.pathsum+Dist[cur_node.end][next_city]	#更新当前走过的路程值
	next_node.end=next_city 			#更新最后一个点
	next_node.num=cur_node.num+1		#更新走过的城市数量
	next_node.listc=cur_node.listc.copy()
	next_node.listc.append(next_city)	#更新走过的城市的路径
	next_node.visited=cur_node.visited.copy()
	next_node.visited[next_city] = True	#将nextcity标为已经走过了
	next_node.lb = get_lb(next_node);	#求目标函数

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
	Path_Up=get_up(CityNum,Dist)

	node=Node(CityNum)	#出发城市的节点信息
	node.end=0 			#结束点到0结束(当前路径的结束点)
	node.num+=1 		#遍历过得点数，初始1个
	node.listc.append(0)
	node.visited[0]=True
	node.lb=Path_Up 	#初始目标值等于上界
	
	Min_Path=math.inf 	#Min_Path是问题的最终解
	pri_queue = Queue() #创建一个优先队列
	pri_queue.put(node) #将起点加入队列
	while pri_queue.qsize()!=0: 
		cur_node=pri_queue.get()
		#判断是否将所有城市都遍历完成
		if cur_node.num==CityNum:
			ans=cur_node.pathsum+Dist[cur_node.start][cur_node.end]	 	#总的路径消耗
			Path_Up=min(ans,Path_Up)				#上界更新为更接近目标的ans值
			if(Min_Path>ans):
				Min_Path=ans
				BestPath=cur_node.listc.copy()

		#当前点可以向下扩展的点入优先级队列
		for i in range(CityNum):
			if cur_node.visited[i]==False:
				next_node=create_node(cur_node,i)
				if next_node.lb>=Path_Up:
					continue
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
	ResultShow(Min_Path,BestPath,CityNum,"分支限定法")
	print("程序的运行时间是：%s"%(end-start))
	draw(BestPath,Position,"Branch And Bound Method")
"""
结果：
贪心法求得最短旅行商经过所有城市回到原城市的最短路径为：
0->4->6->7->1->3->2->5->8->9->0
总路径长为：10127.552143541276

程序的运行时间是：0.10620661
"""
