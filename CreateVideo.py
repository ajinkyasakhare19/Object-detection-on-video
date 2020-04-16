# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 03:11:23 2020

@author: ajink
"""
import cv2
import pandas as pd 

path='C:/Users/ajink/RTAIAssignment2/car_detection_in_video-master/out/'
data = pd.read_csv("Q3_vid.csv")
#data = data[~data['start'].isnull()]
font= cv2.FONT_ITALIC
fontScale= 0.3
fontColor= (0,0,0)
lineType=1
print(data)
color = (255, 0, 0) 
thickness = 0
img_array = []
for index, row in data.iterrows():
    #print(row['FNo'], row['start'],row['end'],row['ObjectColour'],row['Type'])
    img = cv2.imread(path+str(row['FNo'])+".jpg")
    height, width, layers = img.shape
    size = (width,height)

       
    if isinstance(row['start'],str)==False:
        start_point=(0,0)
        end_point=(0,0)
    else:
        
        start_point=eval(row['end'])
        end_point=eval(row['start']) 
        start_point=(start_point[0],end_point[1])
        end_point=(start_point[1],end_point[0])
    img=cv2.rectangle(img, start_point, end_point, color, thickness)
    a=str(row['ObjectColour'])+":"+str(row['Type'])
    cv2.putText(img,a,start_point,font,fontScale,fontColor,lineType)
    img_array.append(img)
out = cv2.VideoWriter('C:/Users/ajink/RTAIAssignment2/car_detection_in_video-master/out/out.mp4',cv2.VideoWriter_fourcc(*'mp4v'),25, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()
