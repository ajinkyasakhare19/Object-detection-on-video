# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 13:34:50 2020

@author: ajink
"""

import numpy as np
from PIL import Image
import cv2

class DetectColour():
    def __init__(self):
        self.MyColourRange={
        'Black':(np.array([  0,   0,  27]), np.array([131,  65,  65])),
        'Silver':(np.array([117,   0, 122]), np.array([255,  19, 255])),
        'Red':(np.array([155,  56,  60]), np.array([190, 170, 197])),
        'White':(np.array([ 73,   0, 178]), np.array([140,  21, 255])),
        'Blue':(np.array([ 67,  23,  66]), np.array([116, 106, 255])),
        }
    
    def get_hsv(self,image):#Get HSV Values for image given 
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        return hsv
    
    def get_colour(self,hsv):#This function is use to get the colour value
        PixleNumbers=0#Initiate number of pixel of each colour range specified
        for colour in self.MyColourRange:#Iterate through each colour range
            #Mask each colour on hsv output
            mask = cv2.inRange(hsv, self.MyColourRange[colour][0], self.MyColourRange[colour][1])
            
            # Get the number of pixel applied after mask
            PixelsValues = np.sum(mask == 255) / 255
            #verify which colour value dominate among the six values specified
            if PixelsValues > PixleNumbers:
                car_colour = colour
                PixleNumbers = PixelsValues        
                    
        return(car_colour)#retrun colour name from range specified

"""#read image file using cv2
image = cv2.imread('C:\\Users\\ajink\\RTAIAssignment2\\Out\\266.png')
#Create an object of detect colour class
detect=DetectColour()
#Get the hsv value of given image
hsv=detect.get_hsv(image)
#Get the colour of object(Car) from image
colour=detect.get_colour(hsv)
print(colour)#print colour"""