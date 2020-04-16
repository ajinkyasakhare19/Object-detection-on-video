# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 16:45:29 2020

@author: ajink / manivs
"""

import cv2
import csv
import argparse
from DetectColour import DetectColour
from DetectCar import DetectCar
# Begin Mani
from datetime import datetime
import time
from DetectCartype import DetectCartype
from multiprocessing import Process, Queue

# End

#Begin Mani
video = "./video.mp4"
#End
#Create an object of detect car class
detect_car = DetectCar()
#Create an object of detect colour class
detect_colour =DetectColour()
#Start Mani
detect_cartype = DetectCartype()

def wirteData(csv_file,csv_columns,dict_data):
    #csv writer logic
    try:
        print("Writing Data")
        with open(csv_file, 'w',newline='') as csvfile:#Open csv file
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)#create CSV writer object
            writer.writeheader()#Wirite coloum header 
            for data in dict_data:#loop thru list of dictionaries
                writer.writerow(data)#Write dict as row
    except IOError:
        print("I/O error")
    
#-------------------------------------
#Video to frame converter
#-------------------------------------
def videoFrame(frame_queue):
    frame_no = 1
    video_capture = cv2.VideoCapture(video)#Open Video
    while video_capture.isOpened():#read whilte video is open
        ret, frame = video_capture.read()#read each frame
        
        if ret == True:
            #Write images on output location
            #cv2.imwrite('C:\\Users\\ajink\\RTAIAssignment2\\car_detection_in_video-master\\out\\'+str(frame_no)+'.jpg',frame)
            frame_queue.put(frame)#fass frame to frame quque
            print(frame_no)#print frame no
            frame_no+=1#increase frame count
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break
    #Once the video is over release video capture
    video_capture.release()
    # Closes all the windows
    cv2.destroyAllWindows()
            
#-------------------------------------
#Target function for Q1
#-------------------------------------
def videoProcessorQ1(frame_queue1,frame_queue_1,frame_queue_2,r1):
    frame_no = 1
    result=[]
    while True:
        objectCount={}#Define result dectionary for frame

        if (frame_queue1.empty()==False):#process while queue is empty
            frame1=frame_queue1.get()#Get item(Frame) from queue
            seconds = datetime.now()#get current time
            frame_details = detect_car.detect_Car(frame_no, frame1)#Get details of the frame using carDetect class
            frame_queue_1.put(frame_details)#put details in colour detection queue
            frame_queue_2.put(frame_details)#put details in type detection queue
            car_count=len(frame_details.getObjects())#Find count of cars in frame
            objectCount["FNo"]=frame_no#append frame bo to result dectionary for frame
            frame_no+=1#Increase frame number count
            objectCount["ObjectCount"]=car_count#append object count result dectionary for frame
            seconds1 = datetime.now()#End time
            t=seconds1-seconds#time diffrence 
            objectCount["Time"]=t.total_seconds()*1000#set time to result dictionary as microseconds
            
            result.append(objectCount)#Append each frame result to fial result list
            r1.put(objectCount)#Put frame result in result1 queue
            
        else: 
            if frame_no >=1495:#If frame count is more than 1495 write results on file and break
                wirteData("Q1.csv",['FNo', 'ObjectCount', 'Time'],result)
                break
            else:
                pass

#-------------------------------------
#Target function for Q2
#-------------------------------------              
def videoProcessorQ3(frame_queue1,r2):
    frame_no=1
    result=[]
    while True:
        objectCount={}
        colour_list=[]
        if (frame_queue1.empty()==False):#process while queue is empty
            seconds = datetime.now()#get current time
            frame_details=frame_queue1.get()#Get item(Frame) from queue                 
            car_count=len(frame_details.getObjects())#Find count of cars in frame
            objectCount["FNo"]=frame_no#append frame bo to result dectionary for frame
            frame_no+=1#Increase frame number count
            objectCount["ObjectCount"]=car_count#append object count result dectionary for frame
            if car_count<1:#if count is less than one
                seconds1 = datetime.now()#get current time
                t=seconds1-seconds#time diffrence 
                objectCount["Time"]=t.total_seconds()*1000#set time to result dictionary as microseconds
                objectCount["ObjectColour"]="NA"#Set coulor to NA
               
            else:
                    for bounding_box in frame_details.getObjects():#For each object in given frame 
                            #Get the hsv value of given image
                            hsv=detect_colour.get_hsv(bounding_box)
                            #Get the colour of object(Car) from image
                            colour=detect_colour.get_colour(hsv)
                            colour_list.append(colour)#Append the colour to list
                    seconds1 = datetime.now()
                    objectCount["ObjectColour"]=colour_list
                    t=seconds1-seconds#time diffrence 
                    objectCount["Time"]=t.total_seconds()*1000#set time to result dictionary as microseconds
            result.append(objectCount)#Append each frame result to fial result list
            r2.put(objectCount)#Put frame result in result2 queue
        else: 
            if frame_no >=1495:#If frame count is more than 1495 write results on file and break
                wirteData("Q3.csv",['FNo', 'ObjectCount', 'Time',"ObjectColour"],result)
                break
            else:
                pass
                
#-------------------------------------
#Target function for Q3
#-------------------------------------                
def videoProcessorQ2(frame_queue1,r3):
    frame_no=1
    result=[]
    while True:
        objectCount={}
        car_list=[]

        if (frame_queue1.empty()==False):#process while queue is empty
                seconds = datetime.now()#get current time
                frame_details=frame_queue1.get()#Get item(Frame) from queue     
                car_count=len(frame_details.getObjects())#Find count of cars in frame
                objectCount["FNo"]=frame_no#append frame bo to result dectionary for frame
                objectCount["ObjectCount"]=car_count#append object count result dectionary for frame
                frame_no+=1#Increase frame number count
                if car_count<1:#if count is less than one
                    seconds1 = datetime.now()#get current time
                    t=seconds1-seconds#time diffrence 
                    objectCount["Time"]=t.total_seconds()*1000#set time to result dictionary as microseconds
                    objectCount["Type"]="NA"#Set type to NA
                    objectCount["Boxes"]="NA"#set bounding boxes to NA
                else:
                    for bounding_box in frame_details.getObjects():#For each object in given frame
                            car_type = detect_cartype.predict_cartype(bounding_box)#Predict car type
                            if car_type == "Hatchback":
                                  objectCount["Type"]=car_list#Set type 
                                  car_list.append(car_type)#append result to list
                            else:
                                objectCount["Type"]=car_list#Set type
                                car_list.append(car_type)#append result to list
                    seconds1 = datetime.now()#Find time now
                    objectCount["Boxes"]=frame_details.getRect()#set boxes
                    t=seconds1-seconds#get time diffrence 
                    objectCount["Time"]=t.total_seconds()*1000#set time to result dictionary as microseconds
                    
                    
                result.append(objectCount)
                r3.put(objectCount)
        else: 
            if frame_no >=1495:#If frame count is more than 1495 write results on file and break
                 wirteData("Q2.csv",['FNo', 'ObjectCount', 'Time',"Type","Boxes"],result)
                 break
            else:
                pass
                #print("\nWaiting for item in Q3 queue\n")
#-------------------------------------
#Target function for Printing data
#-------------------------------------
def printData(Query,r1,r2,r3):
    frame_no=1
    results=[]
    resultsT=[]
    
    while True:
        times={}#get timees dictionary 
        colour_types = {  'Black':0,
            'Silver':0,
            'Red':0,
            'White':0,
            'Blue':0
            }
        #initialize result row
        result_row = {  "FrameNo":frame_no, 
                        "Sedan": colour_types.copy(), 
                        "Hatchback": colour_types.copy(), 
                        "Total":0
                        }
        if(r1.empty()==False):#check if queue is empty
            r1_obj=r1.get()#get item from result1 queue
            r2_obj=r2.get()#get item from result1 queue
            r3_obj=r3.get()#get item from result1 queue
            if Query==3:#Check query option 
                print("\n--------------")
                print("Query fired:",Query)
                print("--------------")
                print("Frame No: "+str(r1_obj["FNo"])+"\nCar Count: "+str(r1_obj["ObjectCount"])+"\nCar Clolour: "+str(r2_obj["ObjectColour"])+"\nCar Type: "+str(r3_obj["Type"])+"\nQ3 Time: "+str(r1_obj["Time"]+r2_obj["Time"]+r2_obj["Time"]))
                time.sleep(0.5)
            elif Query==2:
                print("\n--------------")
                print("Query fired:",Query)
                print("--------------")
                print("Frame No: "+str(r1_obj["FNo"])+"\nCar Count: "+str(r1_obj["ObjectCount"])+"\nCar Type: "+str(r3_obj["Type"])+"\nQ2 Time: "+str(r1_obj["Time"]+r2_obj["Time"]))
                time.sleep(0.5)
            elif Query==1:
                print("\n--------------")
                print("Query fired:",Query)
                print("--------------")
                print("Frame No: "+str(r1_obj["FNo"])+"\nCar Count: "+str(r1_obj["ObjectCount"])+"\nQ1 Time: "+str(r1_obj["Time"]))
                time.sleep(0.5)
            times["Frame No"]=str(r1_obj["FNo"])#set frame no for times dict
            times["Q1"]=int(r1_obj["Time"])#set Q1 time for times dict
            times["Q2"]=int(r1_obj["Time"]+r3_obj["Time"])#set Q1+Q2 time for times dict
            times["Q3"]=int(r1_obj["Time"]+r2_obj["Time"]+r3_obj["Time"])#set Q1+Q2+Q3 time for times dict
            if r1_obj["ObjectCount"]<1:#If object count less than one 
                result_row["FrameNo"]=r1_obj["FNo"]
                result_row["Total"]=r1_obj["ObjectCount"]
            else:
                for colour,ctype in zip(r2_obj["ObjectColour"],r3_obj["Type"]):
                    colour_types[colour]+=1
                    result_row[ctype]=colour_types.copy()
                result_row["FrameNo"]=r1_obj["FNo"]
                result_row["Total"]=r1_obj["ObjectCount"]
            results.append(result_row)#append results
            resultsT.append(times)#append time results      
            frame_no+=1#increase frame count
        else:#If frame count is more than 1495 write results on file and break
            if frame_no >=1494:
               with open('predictions.csv', 'w', newline='') as f:
                   writer = csv.writer(f)
                   for result_row in results:
                       csv_row = []
                       csv_row.append(result_row["FrameNo"])
                       for colour_count in result_row["Sedan"].values():
                           csv_row.append(colour_count)
                       for colour_count in result_row["Hatchback"].values():
                           csv_row.append(colour_count)
                       csv_row.append(result_row["Total"])
                       writer.writerow(csv_row)
               wirteData("Times.csv",['Frame No', 'Q1', 'Q2',"Q3"],resultsT)
               break
            else:
                print("\nWaiting for items\n")
     
    
def main():
    
    # Get arguments from command line ...
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--query", 
                    help="query")
    args = parser.parse_args()
    Query=int(args.query)#Convert command line arg to int
    print(type(Query))
    frame_queue = Queue()#Create Frame queue
    frame_queue_1 = Queue()#Creare Queue for Query 2
    frame_queue_2 = Queue()#Creare Queue for Query 3
    
    r1 = Queue()#Queue for result of Q1
    r2 = Queue()#Queue for result of Q2
    r3 = Queue()#Queue for result of Q3
    

    p1=Process(target=videoFrame, args=(frame_queue,))#Create process for video to frame conversion
    #Create process for Q1
    p2=Process(target=videoProcessorQ1, args=(frame_queue,frame_queue_1,frame_queue_2,r1))
    #Create process for Q2
    p3=Process(target=videoProcessorQ3, args=(frame_queue_1,r2))
    #Create process for Q3
    p4=Process(target=videoProcessorQ2, args=(frame_queue_2,r3))
    #Create process for printing results
    p5=Process(target=printData, args=(Query,r1,r2,r3))

    #Start process P1
    p1.start()
    #Sleep for 2 sec
    time.sleep(2)
    #Start process P2
    p2.start()
    print("Q1 Start")
    #Start process P3
    p3.start()
    print("Q2 Start")
    #Start process P4
    p4.start()
    print("Q3 Start")
    time.sleep(4)
    #Join all processes
    p5.start()
    p1.join()
    p2.join() 
    p3.join()
    p4.join()

if __name__ == "__main__":
    print("Start")
    #Get initial time
    seconds = time.time()
    #Call main 
    main()
    #get end time of execution
    seconds1 = time.time()
    print("-->Total time taken:",seconds1-seconds)