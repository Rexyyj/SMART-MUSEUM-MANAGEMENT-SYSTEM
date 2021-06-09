# -*- coding: utf-8 -*-
"""
Created on Thu May  6 00:17:44 2021

@author: shao
"""

from common.RegManager import *
from common.MyMQTT import *
from common.Mapper import Mapper
from thinkSpeak.ThingSpeakChannel import TSchannel
import json
import time
import requests
import datetime
import threading
 
    
class Lightcontrol():
    def __init__(self,confAddr):
        try:
            self.conf = json.load(open(confAddr))
        except:
            print("Configuration file not found")
            exit()
        self.workingStatus = True
        self.homeCatAddr = self.conf["homeCatAddress"]
        self.clientID = self.conf["serviceId"]
        self.port = self.conf["port"]
        self.topic = self.conf["topicPub"]
        self.broker = self.conf["broker"]
        self.client = MyMQTT(self.clientID, self.broker, self.port, self)
        self.mapper = Mapper()
        # Register service to homeCat
        regMsg = {"registerType": "service",
                  "id": self.clientID,
                  "type": "lightcontrol",
                  "attribute": None}
        self.Reg = RegManager(self.homeCatAddr)
        self.museumSetting = self.Reg.register(regMsg)
        # check the register is correct or not
        if self.museumSetting == "":
            exit()
        # get all available light device from homeCat
        self.devices = self.Reg.getData("devices", "light", None)["data"]
        
        self.zone2light = self.mapper.getMap_zone2Light(self.devices,self.museumSetting["zones"])
        self.zones = {}
        for zoneDef in set(self.museumSetting["zones"].keys()):
            self.zones[zoneDef] = 0

        thingspeak = self.Reg.getData("service","thingspeak",None)["data"][0]
        channels = thingspeak["attribute"]["channels"]
        self.tschannels ={}
        for channel in channels:
            self.tschannels[channel["name"]] = TSchannel(config=thingspeak["attribute"]["config"],channelInfo=channel)

    def start(self):
        self.client.start()
        self.client.mySubscribe(self.conf["topicSub"])

    def stop(self):
        self.client.stop()
   
    def publish(self, lightId, brightness):
        msg = {"lightControllerId":lightId,"timestamp":str(datetime.datetime.now()), "brightness":str(brightness)}
        self.client.myPublish(self.topic, msg)
        print("Published: " + json.dumps(msg))


    def judege_light_brightness(self,time,number,origin_brightness):
        brightness =100

        if time > 10 and time< 15:
            brightness = 70

        if number == 0 and origin_brightness >=10 :
            brightness = origin_brightness - 10
        
        return brightness




    def notify(self,topic,msg):
        
        payload=json.loads(msg)    
        timeH = int(time.strftime('%H'))
        for zone in set(payload.keys()):
            self.zones[zone] = self.judege_light_brightness(timeH,payload[zone],self.zones[zone])
            lightId = self.zone2light[zone]
            self.publish(lightId,self.zones[zone])
            time.sleep(0.5)

    
    def thingSpeakUploader(self):
        while self.workingStatus:
            for key in list(self.tschannels.keys()):
                self.tschannels[key].UploadData("light",self.zone[key])
                time.sleep(10)


if __name__=="__main__":
    configFile = input("Enter the location of configuration file: ")
    if len(configFile) == 0:
        configFile = "./configs/lightControl.json"
    lightcontrol = Lightcontrol(configFile)
    
    t = threading.Thread(target=lightcontrol.thingSpeakUploader)
    lightcontrol.start()
    t.start()
    print("Crowd control service running...")
    print("Enter 'q' to exit")
    while (True):
        if input() == 'q':
            break
    
    lightcontrol.stop()