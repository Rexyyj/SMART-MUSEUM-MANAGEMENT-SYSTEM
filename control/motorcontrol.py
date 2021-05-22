# -*- coding: utf-8 -*-
"""
Created on Fri May  7 21:36:02 2021

@author: shao
"""
from RegManager import *
from MyMQTT import *
import json
import time
import requests


 
    
class Healthymanager():
    def __init__(self,clientID,topicID,broker,port):
        self.client=MyMQTT(clientID,self.self.broker,self.port,self)
        #self.regManager=RegManager()
        self.clientID = clientID
        self.port = 1883
        self.topic='/museumId/entranceId'
        self.broker='localhost'  #其他人运行时请修改broker
        self.motor={'motor1status':'open',
                    'motor2status':'open',
                    'motor3status':'open',
                    'motor4status':'open' }
        
                    
                    
                    
                    
        #getdata=self.regManager.get_data()
      
        
    
    def start(self):
        self.client.start()
        self.client.mySubscribe(self.topic)

    def stop(self):
        self.client.stop()

    def notify(self,topic,msg):
        
        payload=json.loads(msg)    
        
        cameraIdID=payload["cameraId"]
        sequenceNum=payload['sequenceNum']  #图片的编号
        temperature=payload['temperature']
        
        if self.cameraIdID == "camera1":
            if temperature >= 37:
                self.motor['motor1status'] = 'close'
                Message={"motroControlerId":"motor1","timestamp":time.time(),"targetStatus":"close"}
                self.client.myPublish("yourtopic",json.dumps(Message))
            elif temperature < 37:
                Message={"motroControlerId":"motor1","timestamp":time.time(),"targetStatus":"open"}
                self.client.myPublish("yourtopic",json.dumps(Message))
        elif self.cameraIdID == "camera2":
                 if temperature >= 37:
                     self.motor['motor2status'] = 'close'
                     Message={"motroControlerId":"motor2","timestamp":time.time(),"targetStatus":"close"}
                     self.client.myPublish("yourtopic",json.dumps(Message))
                 elif temperature < 37:
                     Message={"motroControlerId":"motor2","timestamp":time.time(),"targetStatus":"open"}
                     self.client.myPublish("yourtopic",json.dumps(Message))
        elif self.cameraIdID == "camera3":
                 if temperature >= 37:
                     self.motor['motor3status'] = 'close'
                     Message={"motroControlerId":"motor3","timestamp":time.time(),"targetStatus":"close"}
                     self.client.myPublish("yourtopic",json.dumps(Message))
                 elif temperature < 37:
                     Message={"motroControlerId":"motor3","timestamp":time.time(),"targetStatus":"open"}
                     self.client.myPublish("yourtopic",json.dumps(Message))
        elif self.cameraIdID == "camera4":
                 if temperature >= 37:
                     self.motor['motor4status'] = 'close'
                     Message={"motroControlerId":"motor4","timestamp":time.time(),"targetStatus":"close"}
                     self.client.myPublish("yourtopic",json.dumps(Message))
                 elif temperature < 37:
                     Message={"motroControlerId":"motor4","timestamp":time.time(),"targetStatus":"open"}
                     self.client.myPublish("yourtopic",json.dumps(Message))
                     
        
         
            


        
        self.client.myPublish("yourtopic",json.dumps(self.zone))#传输topic需要跟thinkspeak  
        
        


if __name__=="__main__":
    #manager=RegManager('172.0.0.1:8080')
    #getdata=manager.getData('devices','type','floor=2&enterZone=zone1')
    #topic = getdata["topic"]
    port = 1883
    topic='/museumId/entranceId'
    broker='localhost'
    yourtest = Healthymanager("motorcontrol",topic, broker, port)
    yourtest.start()
    
    while (True):
        pass
