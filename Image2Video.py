# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 17:19:36 2020

@author: ajink
"""

import cv2
import numpy as np
import pandas as pd
path="C:\\Users\\ajink\\RTAIAssignment2\\car_detection_in_video-master\\out\\"
data=pd.read_csv("C:\\Users\\ajink\\RTAIAssignment2\\car_detection_in_video-master\\car_detection_in_video-master\\Q3_vid.csv")
frame_no=1
img_array=[]
thickness = 0.1
# Write some Text

font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 0.5
fontColor = (0,0,0)
lineType = 1
for index, row in data.iterrows():

    img = cv2.imread(path+str(row["FNo"])+".jpg")
    height, width, layers = img.shape
    size = (width,height)
    if row["ObjectCount"]<1:
        start_point = (0, 0) 
        end_point = (0, 0) 
    else:
        start_point=eval(row["end"])
        end_point=eval(row["start"])
        end_point=(start_point[1],end_point[0])
        start_point=(start_point[1],end_point[1])
    lable=str(row["Type"])+":"+str(row["ObjectColour"])
    carcount="Car Count: "+str(row["ObjectCount"])
    img=cv2.putText(img,lable, start_point,font,fontScale,fontColor,lineType)
    img=cv2.putText(img,carcount,(240,240),font,fontScale,fontColor,lineType)
    img_array.append(img)
out = cv2.VideoWriter('C:/Users/ajink/RTAIAssignment2/car_detection_in_video-master/out/project.mp4',cv2.VideoWriter_fourcc(*'DIVX'),10, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()