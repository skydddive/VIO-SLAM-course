# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 18:18:24 2017

@author: hyj
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from GeometryLib import  drawCoordinateFrame, euler2Rbn,euler2Rnb
import transformations as tf

import os
#filepath=os.path.abspath('.')  #表示当前所处的文件夹的绝对路径
filepath=os.path.abspath('..')  #表示当前所处的文件夹上一级文件夹的绝对路径

point_id=[]
x=[]
y=[]
z=[]                                                                                                

with open(filepath + '/all_points.txt', 'r') as f:
    data = f.readlines()  #txt中所有字符串读入data  
  
    for line in data:  
        odom = line.split()        #将单个数据分隔开存好  
        numbers_float = map(float, odom) #转化为浮点数  
        x.append( numbers_float[0] )
        y.append( numbers_float[1] )
        z.append( numbers_float[2] )

    
position = []
quaterntions = []
timestamp = []
qw_index = 1
with open(filepath + '/cam_pose.txt', 'r') as f:   #   imu_circle   imu_spline

    data = f.readlines()  #txt中所有字符串读入data    
    for line in data:  
        odom = line.split()        #将单个数据分隔开存好  
        numbers_float = map(float, odom) #转化为浮点数  

        #timestamp.append( numbers_float[0])        
        quaterntions.append( [numbers_float[qw_index], numbers_float[qw_index+1],numbers_float[qw_index+2],numbers_float[qw_index+3]   ] )   # qw,qx,qy,qz
        position.append( [numbers_float[qw_index+4], numbers_float[qw_index+5],numbers_float[qw_index+6] ] )              

px_index = 1
position1 = []
quaterntions1 = []
timestamp1 = []
## imu_int_pose_eulerIntegraton
with open(filepath + '/pose_output.txt', 'r') as f:  # imu_pose   imu_spline
    data = f.readlines()  # txt中所有字符串读入data
    for line in data:
        odom = line.split()
        numbers_float = map(float, odom)
        quaterntions1.append( [numbers_float[px_index+6], numbers_float[px_index+3],numbers_float[px_index+4],numbers_float[px_index+5]   ] )   # qw,qx,qy,qz
        position1.append([numbers_float[px_index], numbers_float[px_index + 1], numbers_float[px_index + 2]])        

## plot 3d        
fig = plt.figure()
plt.ion()
ax = fig.gca(projection='3d')

ax.set_xlabel('X')     
ax.set_ylabel('Y')
ax.set_zlabel('Z')
rpy = []
t = []

rpy1 = [] 
t1 = []
for i in range(0,400,5):
    ax.clear()    
    ax.scatter(x, y, z,c='g')
    
    x1=[]
    y1=[]
    z1=[]    
    rpy.append( tf.euler_from_quaternion(quaterntions[i]) )
    t.append( position[i] )
    p = position[i]
    for j in range(len(rpy)):
        drawCoordinateFrame(ax, rpy[j], t[j])    

    rpy1.append( tf.euler_from_quaternion(quaterntions1[i]) )
    t1.append( position1[i])    
    p1 = position1[i]
    for k in range(len(rpy1)):
        drawCoordinateFrame(ax, rpy1[k], t1[k])
    
    # s = filepath + '/keyframe/all_points_' +str(i)+'.txt'
    # with open(s, 'r') as f:   
    #     data = f.readlines()  #txt中所有字符串读入data  
    #     for line in data:  
    #         odom = line.split()        #将单个数据分隔开存好  
    #         numbers_float = map(float, odom) #转化为浮点数  
    #         x1.append( numbers_float[0] )
    #         y1.append( numbers_float[1] )
    #         z1.append( numbers_float[2] )
            
    #         ax.plot( [ numbers_float[0],   p[0]  ] , [ numbers_float[1], p[1] ] , zs=[ numbers_float[2], p[2] ] )

    s = filepath + '/house_model/house.txt'
    with open(s, 'r') as f:
        data = f.readlines()  # txt中所有字符串读入data
        for line in data:
            odom = line.split()  # 将单个数据分隔开存好
            numbers_float = map(float, odom)  # 转化为浮点数
            ax.plot([numbers_float[0], numbers_float[3]], [numbers_float[1], numbers_float[4]],'b' ,zs=[numbers_float[2], numbers_float[5]])
        
    ax.scatter(x1, y1, z1,c='r',marker='^')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim(-25, 25)
    ax.set_ylim(-25, 25)
    ax.set_zlim(0, 25)
    ax.legend()
    plt.show() 
    plt.pause(0.001)
    
plt.pause(0)    
