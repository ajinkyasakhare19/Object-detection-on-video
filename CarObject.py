# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 18:43:37 2020

@author: ajink
"""

class CarObject():
    def __init__(self,box,name):
        self.box=box
        self.name=name
        
    def getBox(self):
        return self.box
    
    def getName(self):
        return self.name
    
    def setBox(self,box):
         self.box=box
    
    def setName(self,name):
        self.name=name
    