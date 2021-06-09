# -*- coding: utf-8 -*-
"""
Created on Thu May  6 00:17:44 2021

@author: shao
"""

        
from RegManager import *
from MyMQTT import *
import json
import time
import requests
import datetime


class lightcontrol():
    def __init__(self, clientID, topic, broker, port):
        self.homeCatAddr = "http://localhost:8090"
        self.clientID = clientID
        self.port = port
        self.topic = topic
        self.broker = broker
        self.client = MyMQTT(clientID, self.broker, self.port, self)
        # Register service to homeCat
        regMsg = {"registerType": "service",
                  "id": self.clientID,
                  "type": "light",
                  "attribute": {}}
        self.Reg = RegManager(self.homeCatAddr)
        self.museumSetting = self.Reg.register(regMsg)
        # check the register is correct or not
        if self.museumSetting == "":
            exit()
        # get all available light device from homeCat
        self.devices = self.Reg.getData("devices", "light", None)["data"]
        # create a device id to light map in format {"light1":{"controlZone":"zone1",}}
        self.devicelights = {}
        for dev in self.devices:
            self.devicelights[dev["id"]] = dev["attribute"]["controlZone"]
        self.zone2light={}
        for lightkey in self.devicelights.keys():
            self.zone2light[self.devicelights[lightkey]]=lightkey #this dic key is zoneID :lightID


    
    def start(self):
        self.client.start()
        # subscribe to topic according to available device
        
        self.client.mySubscribe(self.topic)

    def stop(self):
        self.client.stop()
        # unregister device
        self.Reg.delete("service", self.clientID)

    
    def notify(self, topic, msg):
        
        zonepeoplenumber = json.loads(msg)#zone{zone1:"xx",zone2:"xx"....}
        brightness={}
        
        curr_time = datetime.datetime.now()
        curr_hour=int(datetime.datetime.now().hour)#get time now  curr_hour range is 0-24
        
        
        for zone in zonepeoplenumber.keys():
            lightID=self.zone2light[zone] #find which light will be processed
            if curr_hour<=12:
                if zonepeoplenumber[zone]==0:
                    brightness_temp=0
                    brightness[lightID]=brightness_temp
                    Message={"lightControllerId":["lightID",lightID],"timestamp":time.time(),"brightness":0}
                    self.client.myPublish("/Polito/iot/SMMS/museum01/lightTopic",json.dumps(Message))
                else:
                    brightness_temp=40
                    brightness[lightID]=brightness_temp
            elif curr_hour>12 and curr_hour<=17:  
                if zonepeoplenumber[zone]==0:
                    brightness_temp=0
                    brightness[lightID]=brightness_temp
                    Message={"lightControllerId":["lightID",lightID],"timestamp":time.time(),"brightness":0}
                    self.client.myPublish("/Polito/iot/SMMS/museum01/lightTopic",json.dumps(Message))
                else:
                     brightness_temp=80
                     brightness[lightID]=brightness_temp
            elif curr_hour>17:                    #evening
                if zonepeoplenumber[zone]==0:
                     brightness_temp=0
                     brightness[lightID]=brightness_temp
                     Message={"lightControllerId":["lightID",lightID],"timestamp":time.time(),"brightness":0}
                     self.client.myPublish("/Polito/iot/SMMS/museum01/lightTopic",json.dumps(Message))
                else:
                     brightness_temp=100
                     brightness[lightID]=brightness_temp
             
        
        
        print("Received: " + json.dumps(zonepeoplenumber, indent=4))
        print("Processed: " + json.dumps(brightness, indent=4))
        print("current time:",curr_time)
        self.client.myPublish("yourtopic",json.dumps(brightness))#传输topic需要跟thinkspeak  
    


if __name__=="__main__":

    port = 1883
    topic='/Polito/iot/SMMS/museum01/zoomcount'
    broker='localhost' #其他人运行时请修改
    yourtest = lightcontrol("lightControllerId",topic,broker,port)
    yourtest.start()
    
    while (True):
        pass
