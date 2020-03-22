# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 16:45:29 2020

@author: ajink
"""
from yolo import YOLO 
from PIL import Image
import cv2
import numpy as np
import argparse
from DetectColour import DetectColour

# Get arguments from command line ...
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--video", 
                    help="Video file location")
parser.add_argument("-o", "--out",
                    help="Output file location")

args = parser.parse_args()
video=args.video
yolo = YOLO()
#Create an object of detect colour class
detect=DetectColour()


Black=(np.array([  0,   0,  27]), np.array([131,  65,  65]))
Silver=(np.array([117,   0, 122]), np.array([255,  19, 255]))
Red=(np.array([155,  56,  60]), np.array([190, 170, 197]))
White=(np.array([ 73,   0, 178]), np.array([140,  21, 255]))
Blue=(np.array([ 67,  23,  66]), np.array([116, 106, 255]))


def main():
    video_capture = cv2.VideoCapture(video)

    out=args.out

    count=0
    while True:
        # Capture the input video frame by frame
        ret, frame = video_capture.read()
        if ret == True:
            
            image = Image.fromarray(frame) # Get each frame of video
            
            r_image, object_boxes, time_value = yolo.detect_image(image) #Detect objects from frame and retun image and coordinates with class
            result = np.asarray(r_image)#Save resulting image 
            print('Size of box {}'.format((object_boxes))) #Print Box size
            
            cv2.imshow("Yolo Test", result) #Show the result image with detected object.
            # Use Q to quit from the window
            for object_box in object_boxes:#For each object in given frame 
                if object_box['class'] == 'car': #Select object with only car as class
                    print('Found a car in frame')
                    top = object_box['top']-20
                    left = object_box['left']
                    bottom = object_box['bottom']
                    right = object_box['right']
                    bounding_box = frame[top:bottom, left:right] # Resulting image of car
                    
                    #Get the hsv value of given image
                    hsv=detect.get_hsv(bounding_box)
                    #Get the colour of object(Car) from image
                    colour=detect.get_colour(hsv)
                    print(colour)#print colour
                    cv2.imshow("Bounding box", bounding_box)#Show image in new window
                    cv2.imwrite(out+str(count)+'.png',bounding_box) #Save image on out directory
                    print("<---- Frame Processed----->")
                    count=count+1 #Increase the count
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        # Break the loop
        else: 
            break
            
    #Once the video is over release video capture
    video_capture.release()
    # Closes all the windows
    cv2.destroyAllWindows()
 
if __name__ == "__main__":
    main()
 