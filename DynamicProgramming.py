# -*- coding: utf-8 -*-
"""
	基于动态规划的旅行商问题解法Python源码

	Author:	Greatpan
	Date:	2018.10.14
"""
import numpy as np
import math
import time
from MyFuncTool import GetData,ResultShow,draw

def DPMethond(CityNum,Dist,city_start):
	"""
		函数名：DPMethond(CityNum,Dist,city_start)
		函数功能： 动态规划算法的程序入口
			输入	1 CityNum：城市数量
				2 Dist：城市间距离矩阵
				3 city_start:旅行商起始城市
			输出	1 Min_Path：最优路径长
				2 BestPath：最优路径
		其他说明：无
	"""
	citylists = 2**(CityNum)-1          #初始已遍历城市列表为全部遍历
	
	Min_Path=DP_recursion(city_start,citylists)     #调用动态规划算法
	
	#此块代码块是根据dp_path矩阵找到最优路径
	BestPath=[]
	for i in range(CityNum):
		BestPath.append(city_start)
		city_start=int(dp_path[city_start][citylists])
		citylists=citylists&(~(1<<city_start))
	BestPath.append(city_init)
	return Min_Path,BestPath


def DP_recursion(city_start,citylists):
	"""
		函数名：DP_recursion(city_start,citylists)
		函数功能：  基于递归调用的动态规划算法核心
			输入	1: city_start:旅行商起始城市
				2: citylists:旅行商已经遍历过的城市，其中第i位为1代表城市i已经遍历过
	           		 第i位为0则代表城市i没有遍历(位数从0开始，第0位即最低位代表城市0)
			输出	1: dp_dist[city_start][citylists]:从城市city_start出发
	           		 遍历citylists内包含的各个城市的所花费的最小距离
		其他说明：无
	"""
	#判断是否已经求出从城市city出发遍历citylists内的城市的最短距离
	if IsSolvedMinDist(city_start,citylists):
		return dp_dist[city_start][citylists]
	
	#判断如果只遍历一个出发点城市，是则返回起始城市到开始城市的距离
	if IsOnlyExistCityN(city_init,citylists):
		return Dist[city_init][city_start]
	
	#求解T(vi,V)=min{Dij+T(vj,V-{Vj})},Vj属于V,公式
	dist_sum=math.inf
	for city in range(CityNum):
		if IsVisited(city,citylists):
			dist_temp=DP_recursion(city,Delete(city,citylists))+Dist[city_start][city]
			if dist_temp<dist_sum:
				dist_sum=dist_temp
				dp_path[city_start][citylists]=city
	dp_dist[city_start][citylists]=dist_sum
	
	return dp_dist[city_start][citylists]


def IsSolvedMinDist(city_start,citylists):
	"""
		函数名：IsSolvedMinDist(city_start,citylists)
		函数功能：判断是否已经求出了从城市city_start出发遍历citylists内的城市的最短距离
			输入	1: city_start:旅行商起始城市
				2: citylists:旅行商已经遍历过的城市，其中第i位为1代表城市i已经遍历过
	            第i位为0则代表城市i没有遍历(位数从0开始，第0位即最低位代表城市0)
			输出	1: 是——返回True，否——返回False
		其他说明：无
	"""
	return True if dp_dist[city_start][citylists] != -1 else False


def IsOnlyExistCityN(cityn,citylists):
	"""
		函数名：IsOnlyExistCityN(cityn,citylists)
		函数功能：判断如果只遍历一个出发点城市，是则返回起始城市到出发点城市的距离
			输入	1: city_start:旅行商起始城市
				2: citylists:旅行商已经遍历过的城市，其中第i位为1代表城市i已经遍历过
	            第i位为0则代表城市i没有遍历(位数从0开始，第0位即最低位代表城市0)
			输出	1: 是——返回True，否——返回False
		其他说明：无
	"""
	return True if citylists==2**cityn else False


def IsVisited(city,citylists):
	"""
		函数名：IsVisited(city,citylists)
		函数功能：判断城市city是否在遍历过的城市列表citylists中
			输入	1: city_start:旅行商起始城市
				2: citylists:旅行商已经遍历过的城市，其中第i位为1代表城市i已经遍历过
	            第i位为0则代表城市i没有遍历(位数从0开始，第0位即最低位代表城市0)
			输出	1: 是——返回True，否——返回False
		其他说明：无
	"""
	return True if citylists&(1<<city) else False


def Delete(city,citylists):
	"""
		函数名：Delete(city,citylists)
		函数功能：从遍历过的城市列表citylists中删去城市city
			输入	1: city_start:旅行商起始城市
				2: citylists:旅行商已经遍历过的城市，其中第i位为1代表城市i已经遍历过
	            第i位为0则代表城市i没有遍历(位数从0开始，第0位即最低位代表城市0)
			输出	1: 删去城市city后的已遍历过城市列表citylists
		其他说明：无
	"""
	return citylists&(~(1<<city))

##############################程序入口#########################################
if __name__ == "__main__":
	Position,CityNum,Dist = GetData("./data/TSP10cities.tsp")
	
	city_init=0                         #起始城市
	
	#dp_path[city][citylists]代表citylists内与city相连的城市信息
	dp_path = np.ones((CityNum,2**CityNum))
	
	#dp_dist[city,citylist]代表从城市city出发经过citylists内走过的城市后返回到city_start的最短距离矩阵
	dp_dist = np.ones((CityNum,2**CityNum))*-1
	
	start = time.clock()				#程序计时开始
	Min_Path,BestPath=DPMethond(CityNum,Dist,city_init)	#调用动态规划算法
	end = time.clock()					#程序计时结束
	
	print()
	ResultShow(Min_Path,BestPath,CityNum,"动态规划法")
	print("程序的运行时间是：%s"%(end-start))
	draw(BestPath,Position,"Dynamic Programming Method")
"""
结果：
贪心法求得最短旅行商经过所有城市回到原城市的最短路径为：
0->4->6->7->1->3->2->5->8->9->0
总路径长为：10127.552143541276

程序的运行时间是：0.064915142
"""
