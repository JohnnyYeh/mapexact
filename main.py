#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :main.py
# @Time      :2022/11
# @Author    :JohnnyYeh

from multiprocessing.connection import wait
import cv2
import numpy as np
import pandas as pd

mode = 1 # 1表示获取道路点模式 2表示获取停靠点模式 3表示获取客户点模式
roadVertexNum = 0 #就是道路各种路口
stoppingPointNum = 0 #停靠点数量
customerNum = 0 #客户点数量

roadVertexArray = []           # road vertex position
stoppingPointArray = []        # stopping point position
customerArray = []             # customer position
stoppingRoadVertexArray = []   # stopping 与 road vertex 之间的关系
RoadVertexRoadVertexArray = [] # road vertex 之间的关系

src = cv2.imread('amcbcmap2.png',1)  # 设置地图的图像
map = src.copy()
windows_name = 'sz_map'
img_size = map.shape
h, w = img_size[0:2]
font = cv2.FONT_HERSHEY_SIMPLEX
lastRoadVertex = (0,0)

def save():
    global roadVertexNum,stoppingPointNum,customerNum
    allVertexNum = roadVertexNum+stoppingPointNum
    print("All vertex number is %d"%allVertexNum)
    
    datas = []
    name = []
    for i in range(allVertexNum):
        name.append(str(i))
        temp = []
        for j in range(allVertexNum):
            temp.append(0)
        datas.append(temp)

    for SR in stoppingRoadVertexArray:
        SRlength  = len(SR)
        for index in range(1,SRlength):
            datas[SR[0]-1][SR[index]+stoppingPointNum-1] = 1
    for RR in RoadVertexRoadVertexArray:
        RRlength = len(RR)
        for index in range(1,RRlength):
            datas[RR[0]+stoppingPointNum-1][RR[index]+stoppingPointNum-1] = 1

    # 停靠点与道路顶点的连接关系，道路顶点与道路顶点的关系
    graphSR = pd.DataFrame(data=datas) 
    print(graphSR)
    graphSR.to_csv('data.csv',encoding='gbk')
    
    name_xy =['x','y']
    # 保存道路顶点位置
    if roadVertexArray:
        roadVertexPosData = pd.DataFrame(columns=name_xy,data=roadVertexArray) 
        roadVertexPosData = pd.DataFrame(data=roadVertexArray) 
        print(roadVertexPosData)
        roadVertexPosData.to_csv('RoadVertexPosData.csv',encoding='gbk')
    else:
        print('RoadVertexPosData is empty')

    # 保存停靠点位置
    if stoppingPointArray:
        stoppingPointPosData = pd.DataFrame(columns=name_xy,data=stoppingPointArray) 
        # stoppingPointPosData = pd.DataFrame(data=stoppingPointArray)
        print(stoppingPointPosData)
        stoppingPointPosData.to_csv('StoppingPointPosData.csv',encoding='gbk')
    else:
        print('StoppingPointPosData is empty')

    # 保存客户点位置
    if customerArray:
        customerPosData = pd.DataFrame(columns=name_xy,data=customerArray)
        print(customerPosData)
        customerPosData.to_csv('CustomerPosData.csv',encoding='gbk')
    else:
        print('CustomerPosData is empty')

def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    global roadVertexNum,stoppingPointNum,customerNum
    # global roadVertexArray,stoppingPointArray,customerArray
    global mode
    global lastRoadVertex 
    if event==cv2.EVENT_LBUTTONDOWN:
        if mode == 1:
            curRoadVertex = (x, y)
            roadVertexArray.append([x, y])
            roadVertexNum += 1
            print("Road vertex number is %d"%roadVertexNum)
            message = '{}'.format(roadVertexNum)
            cv2.putText(map, message, curRoadVertex,
                        font, 0.5, (0,0,0), 1)
            cv2.circle(map, curRoadVertex, 1, (0, 0, 0), -1)
            cv2.imshow(windows_name, map)
            print(curRoadVertex)

        elif mode == 2:
            curStoppingPoint = (x, y)
            stoppingPointArray.append([x, y])
            stoppingPointNum += 1
            print("Stopping point number is %d"%stoppingPointNum)
            message = '{}'.format(stoppingPointNum)
            cv2.putText(map, message, curStoppingPoint,
                        font, 0.5, (255, 0, 0), 1)
            cv2.circle(map, curStoppingPoint, 1, (255, 0, 0), -1)  
            
            print(curStoppingPoint)
            # print("Please input RoadVertex number with respect to curStoppingPoint:")
            num = int(input('Please input RoadVertex number with respect to curStoppingPoint (<4) :'))
            while num > 4:
                num = int(input('Please input RoadVertex number < 4:'))
            temp = [stoppingPointNum]
            for i in range(num):
                index = int(input("Please input RoadVertex index:"))
                while index > roadVertexNum:
                    index = int(input("Please input RoadVertex index < max roadVertexNum:"))
                temp.append(index)
                roadVertex = (roadVertexArray[index-1][0],roadVertexArray[index-1][1])
                cv2.line(map, curStoppingPoint, roadVertex, (255,0,0), 1, 4)
            stoppingRoadVertexArray.append(temp)
            print(stoppingRoadVertexArray)
            cv2.imshow(windows_name, map)

        elif mode == 3:
            curCustomer = (x, y)
            customerArray.append([x, y])
            customerNum += 1
            print("Customer number is %d"%customerNum)
            message = '{}'.format(customerNum)
            cv2.putText(map, message, curCustomer,
                        font, 0.5, (0, 0, 255), 1)
            cv2.circle(map, curCustomer, 1, (0, 0, 255), -1)
            cv2.imshow(windows_name, map)
            print(curCustomer)

        else:
            print('what?')
    
def addVertices():
    global roadVertexNum,stoppingPointNum,customerNum
    # print('Please input the first road vertex (input q will exit):')
    index1 = int(input('Please input the start vertex(<%d):'%roadVertexNum)) 
    roadVertex1 = (roadVertexArray[index1-1][0],roadVertexArray[index1-1][1])

    num = int(input('Please input the number of road vertexs connecting the first road vertex(< 4):'))
    while num > 4:
        num = int(input('Please input the number of road vertexs < 4:'))
    temp = [index1]
    for i in range(num):
        index2 = int(input('Please input the road vertex(<%d):'%roadVertexNum))
        roadVertex2 = (roadVertexArray[index2-1][0],roadVertexArray[index2-1][1])
        cv2.line(map, roadVertex1, roadVertex2, (0,0,0), 1, 4)
        temp.append(index2)
    
    RoadVertexRoadVertexArray.append(temp)
    print(RoadVertexRoadVertexArray)
    cv2.imshow(windows_name, map)

def addVertices2Stops():
    global roadVertexNum,stoppingPointNum,customerNum
    index = int(input('Please input the start stopping point(<%d):'%stoppingPointNum)) 
    stop = (stoppingPointArray[index-1][0],stoppingPointArray[index-1][1])

    num = int(input('Please input the number of road vertexs connecting the stop1(< 4):'))
    while num > 4:
        num = int(input('Please input the number of road vertexs < 4:'))
    temp = [index]
    for i in range(num):
        index = int(input('Please input the road vertex(<%d):'%roadVertexNum))
        roadVertex = (roadVertexArray[index-1][0],roadVertexArray[index-1][1])
        cv2.line(map, stop, roadVertex, (255,0,0), 1, 4)
        temp.append(index)
    
    stoppingRoadVertexArray.append(temp)
    cv2.imshow(windows_name, map)

def main():  
    cv2.imshow(windows_name, map)
    cv2.namedWindow(windows_name)
    cv2.setMouseCallback(windows_name, on_EVENT_LBUTTONDOWN)
    print('Please click image to obtain road vertex position!!')
    global mode
    while True:
        key = cv2.waitKey(20)
        if key  == ord('t'):
            print('Please click image to obtain stopping point position!!')
            mode = 2 
        elif key == ord('c'):
            print('Please click image to obtain customer position!!')
            mode = 3 
        elif key == ord('a'):
            print('Please add relationships between vertices!!')
            addVertices()
        elif key == ord('b'):
            print('Please add relationships between vertices and stops!!')
            addVertices2Stops()
        elif key  == ord('s'):
            print('Saving ...')
            save()
        elif key  == ord('r'):
            print('Restart ...')
            # todo
        elif key == 27:
            break

    cv2.destroyWindow(windows_name)

if __name__ == '__main__':
    main()