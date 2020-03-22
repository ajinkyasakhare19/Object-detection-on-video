# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 18:56:41 2020

@author: ajink
"""

class Frame():
    def __init__(self,frame,objects):
        self.frame=frame
        self.objects=objects
        
    def getFrame(self):
        return self.frame
    
    def getObjects(self):
        return self.objects
    
    def setFrame(self,frame):
         self.frame=frame
    
    def setObjects(self,objects):
        self.objects=objects