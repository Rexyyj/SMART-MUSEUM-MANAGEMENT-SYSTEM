# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 16:45:30 2021

@author: Administrator
"""

from RegManager import *
from MyMQTT import *
import json
import time
import requests


 
    
class Customermanager():
    def __init__(self,clientID,topicID,broker,port):
        self.client=MyMQTT(clientID,self.self.broker,self.port,self)
        #self.regManager=RegManager()
        self.clientID = clientID
        self.port = 1883
        self.topic='/museumId/entranceId'
        self.broker='localhost'
        self.zone={'zone1':0,
                   'zone2':0,
                   'zone3':0,
                   'zone4':0}
        #getdata=self.regManager.get_data()
      
        
    
    def start(self):
        self.client.start()
        self.client.mySubscribe(self.topic)

    def stop(self):
        self.client.stop()

    def notify(self,topic,msg):
        
        payload=json.loads(msg)    
        
        laserID=payload["laserID"]
        enter=payload['enter']
        leaving=payload['leaving']
        
        if laserID == "laser0":
            self.zone['zone1']+=enter
            self.zone['zone1']-=leaving
        elif laserID == "laser1":
            self.zone['zone2']+=enter
            self.zone['zone2']-=leaving
            self.zone['zone1']-=enter
            self.zone['zone1']+=leaving
        elif laserID == "laser2":
            self.zone['zone3']+=enter
            self.zone['zone3']-=leaving
            self.zone['zone2']-=enter
            self.zone['zone2']+=leaving
        elif laserID == "laser3":
            self.zone['zone4']+=enter
            self.zone['zone4']-=leaving
            self.zone['zone3']-=enter
            self.zone['zone3']+=leaving
        else:
            pass
            


        
        self.client.myPublish("yourtopic",json.dumps(self.zone))#传输topic需要跟thinkspeak  
        
        


if __name__=="__main__":
    getdata=RegManager.getData()
    topic = getdata["topic"]
    yourtest = Subscriber("CustormerNumber",topic, broker, port)
    yourtest.start()
    
    while (True):
        pass

 
