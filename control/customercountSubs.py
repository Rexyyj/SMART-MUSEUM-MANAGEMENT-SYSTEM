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

class Subscriber():
    def __init__(self,clientID,self.topic,self.broker,self.portport):
        self.client=MyMQTT(clientID,self.self.broker,self.port,self)
        self.clientID = clientID
        self.port = 1883
        self.topic='/museumId/entranceId'
        self.broker='localhost'
        self.zone={'zone1':0,
                   'zone2':0,
                   'zone3':0,
                   'zone4':0}
        
    
    def start(self):
        self.client.start()
        self.client.mySubscribe(self.topic)

    def stop(self):
        self.client.stop()

    def notify(self,topic,msg):
        
        getdata=RegManager.getData(fatherType, childType, params)
        
         
        enterzone=getdata["attribute"]["enterZone"]
        if enterzone="zone1":
            self.zone['zone1']+=1
        elif enterzone="zone2":
            self.zone['zone2']+=1
        elif enterzone="zone3":
            self.zone['zone3']+=1
        elif enterzone="zone4":
            self.zone['zone4']+=1
        else:
            pass
            

        leavingzone=getdata["attribute"]["leavingZone"]
        if leavingzone="leavingZone1":
            self.zone['zone1']-=1
        elif leavingzone="leavingZone2":
            self.zone['zone2']-=1
        elif leavingzone="leavingZone3":
            self.zone['zone3']-=1
        elif leavingzone="leavingZone4":
            self.zone['zone4']-=1
        else:
            pass
        
        self.client.myPublish("yourtopic",json.dumps(self.zone))#传输topic需要跟thinkspeak  
        
        


if __name__=="__main__":
    yourtest = Subscriber("CustormerNumber", '/museumId/entranceId', broker, port)
    yourtest.start()
    while (True):
        pass

 
