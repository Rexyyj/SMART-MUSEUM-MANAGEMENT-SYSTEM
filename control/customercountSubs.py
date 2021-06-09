# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 16:45:30 2021

@author: Administrator
"""

from common.RegManager import *
from common.MyMQTT import *
from common.Mapper import Mapper
from thinkSpeak.ThingSpeakChannel import  TSchannel
import json
import time
import requests
import threading

class Customermanager():

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
        # Register service to homeCat
        regMsg = {"registerType": "service",
                  "id": self.clientID,
                  "type": "crowdcontrol",
                  "attribute": None}
        self.Reg = RegManager(self.homeCatAddr)
        self.museumSetting = self.Reg.register(regMsg)
        # check the register is correct or not
        if self.museumSetting == "":
            exit()

        self.mapper = Mapper()
        # get all available laser device from homeCat
        self.devices = self.Reg.getData("devices", "laser", None)["data"]
        # create a device id to zone map in format {"laser1":{"enterZone":"zone1","leavingZone":"zone2"}}
        self.device2zone = self.mapper.getMap_device2zone_LM(self.devices)
        # define zone counter from museum setting
        self.zone = {}
        for zoneDef in set(self.museumSetting["zones"].keys()):
            self.zone[zoneDef] = 20
        time.sleep(1)
        # create thingspeak instances
        thingspeak = self.Reg.getData("service","thingspeak",None)["data"][0]
        channels = thingspeak["attribute"]["channels"]
        self.tschannels ={}
        for channel in channels:
            self.tschannels[channel["name"]] = TSchannel(config=thingspeak["attribute"]["config"],channelInfo=channel)


    def start(self):
        self.client.start()
        # subscribe to topic according to available device
        topics = set()
        for dev in self.devices:
            topics.add(dev["topic"])
        for topic in topics:
            self.client.mySubscribe(topic)

    def stop(self):
        self.workingStatus=False
        self.client.stop()
        # unregister device
        self.Reg.delete("service", self.clientID)

    def notify(self, topic, msg):

        payload = json.loads(msg)

        laserID = payload["id"]
        # add int due to joson only transmit string,can not do +- calculation
        enter = int(payload['enter'])
        leaving = int(payload['leaving'])

        self.zone[str(self.device2zone[laserID]["enterZone"])] += enter
        if (self.zone[str(self.device2zone[laserID]["leavingZone"])] - leaving) > 0:
            self.zone[str(self.device2zone[laserID]["leavingZone"])] -= leaving
        else:
            self.zone[str(self.device2zone[laserID]["leavingZone"])] = 0

        print("Received: " + json.dumps(payload, indent=4))
        print("Processed: " + json.dumps(self.zone, indent=4))

        self.client.myPublish(self.topic, json.dumps(self.zone))
        # 传输topic需要跟thinkspeak

    def thingSpeakUploader(self):
        while self.workingStatus:
            for key in list(self.tschannels.keys()):
                self.tschannels[key].UploadData("crowd",self.zone[key])
                time.sleep(10)




if __name__ == "__main__":
    configFile = input("Enter the location of configuration file: ")
    if len(configFile) == 0:
        configFile = "./configs/crowdControl.json"

    customermanager = Customermanager(configFile)
    t = threading.Thread(target=customermanager.thingSpeakUploader)
    customermanager.start()
    t.start()
    print("Crowd control service running...")
    print("Enter 'q' to exit")
    while (True):
        if input() == 'q':
            break
    
    customermanager.stop()
