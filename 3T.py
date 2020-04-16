import cv2
import numpy as np
import glob

img_array = []
for filename in glob.glob('C:/Users/ajink/RTAIAssignment2/car_detection_in_video-master/out/*.jpg'):
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    start_point = (5, 5) 
    end_point = (220, 220) 
    color = (255, 0, 0) 
    thickness = 2
    img=cv2.rectangle(img, start_point, end_point, color, thickness)
    img_array.append(img)


out = cv2.VideoWriter('C:/Users/ajink/RTAIAssignment2/car_detection_in_video-master/out/project.mp4',cv2.VideoWriter_fourcc(*'DIVX'),1, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()