# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 16:45:30 2021

@author: Administrator
"""

from common.RegManager import *
from common.MyMQTT import *
from common.Mapper import Mapper
import json
import datetime
import time
import threading
class Customermanager():

    def __init__(self, confAddr):
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
        self.statusTopic = self.conf["zoneStatusTopic"]
        self.broker = self.conf["broker"]
        self.client = MyMQTT(self.clientID, self.broker, self.port, self)
        self.__msg = {"id": self.clientID,
                      "timestamp": "", "data": ""}
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
        self.zoneStatus = {}
        for zoneDef in (set(self.museumSetting["zones"].keys())-{"outdoor"}):
            self.zone[zoneDef] = 20
            self.zoneStatus = "open"

        self.zoneCapa = self.museumSetting["zones"]
        self.pubCounter = 0

    def start(self):
        self.client.start()
        # subscribe to topic according to available device
        topics = set()
        for dev in self.devices:
            topics.add(dev["topic"])
        for topic in topics:
            self.client.mySubscribe(topic)

    def stop(self):
        self.workingStatus = False
        self.client.stop()
        # unregister device
        self.Reg.delete("service", self.clientID)


    def crowd_publish(self, data):
        msg = self.__msg
        msg["timestamp"] = str(datetime.datetime.now())
        msg["data"] = data
        self.client.myPublish(self.topic, msg)
        print("Published: " + json.dumps(msg))

    def status_publish(self,data):
        msg = self.__msg
        msg["timestamp"] = str(datetime.datetime.now())
        msg["data"] = data
        self.client.myPublish(self.statusTopic, msg)
        print("Published: " + json.dumps(msg))

    def notify(self, topic, msg):

        payload = json.loads(msg)

        laserID = payload["id"]
        # add int due to joson only transmit string,can not do +- calculation
        enter = int(payload['enter'])
        leaving = int(payload['leaving'])

        if self.device2zone[laserID]["enterZone"] == "outdoor":
            pass
        else:
            self.zone[self.device2zone[laserID]["enterZone"]] += enter

        if self.device2zone[laserID]["leavingZone"] == "outdoor":
            pass
        else:
            if (self.zone[self.device2zone[laserID]["leavingZone"]] - leaving) > 0:
                self.zone[self.device2zone[laserID]["leavingZone"]] -= leaving
            else:
                self.zone[self.device2zone[laserID]["leavingZone"]] = 0

        for key in set(self.zone.keys()):
            if int(self.zone[key])>int(self.zoneCapa[key]):
                self.zoneStatus[key] = "close"

        self.crowd_publish(self.zone)
        self.status_publish(self.zoneStatus)




if __name__ == "__main__":
    configFile = input("Enter the location of configuration file: ")
    if len(configFile) == 0:
        configFile = "./configs/crowdControl.json"

    customermanager = Customermanager(configFile)
    customermanager.start()
    print("Crowd control service running...")
    print("Enter 'q' to exit")
    while (True):
        if input() == 'q':
            break

    customermanager.stop()
