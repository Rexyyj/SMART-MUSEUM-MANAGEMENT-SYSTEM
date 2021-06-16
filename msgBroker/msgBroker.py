# -*- coding: utf-8 -*-
# @Time    : 6/5/2021 3:08 PM
# @Author  : Rex Yu
# @Mail    : jiafish@outlook.com
# @Github  : https://github.com/Rexyyj

from common.RegManager import *
from common.MyMQTT import *
from common.Mapper import Mapper
from thinkSpeak.ThingSpeakChannel import TSchannel
import json
import time
import threading


class MsgBroker():

    def __init__(self,confAddr):
        try:
            self.conf = json.load(open(confAddr))
        except:
            print("Configuration file not found")
            exit()
        self.workingStatus = True
        self.homeCatAddr = self.conf["homeCatAddress"]
        self.serviceID = self.conf["serviceId"]
        self.port = self.conf["port"]
        self.broker = self.conf["broker"]
        self.client = MyMQTT(self.serviceID, self.broker, self.port, self)
        self.crowdTopic = self.conf["crowdTopic"]
        self.ligthTopic = self.conf["lightTopic"]
        self.statusTopic = self.conf["statusTopic"]

        # Register service to homeCat
        regMsg = {"registerType": "service",
                  "id": self.serviceID,
                  "type": "msgBroker",
                  "attribute": None
                  }
        self.Reg = RegManager(self.homeCatAddr)
        self.museumSetting = self.Reg.register(regMsg)
        # check the register is correct or not
        if self.museumSetting == "":
            exit()

        self.mapper = Mapper()
        self.lights = self.Reg.getData("devices", "light", None)["data"]
        self.light2zone = self.mapper.getMap_light2zone(self.lights)

        thingspeak = self.Reg.getData("service","thingspeak",None)["data"][0]
        channels = thingspeak["attribute"]["channels"]
        self.tschannels ={}
        for channel in channels:
            self.tschannels[channel["name"]] = TSchannel(config=thingspeak["attribute"]["config"],channelInfo=channel)
        
        # init data aggregator
        self.data = {}
        for zoneDef in (set(self.museumSetting["zones"].keys())-{"outdoor"}):
            self.data[zoneDef] = {"crowd":20,"light":100,"status":1}

        
    def start(self):
        self.client.start()
        # subscribe to topic according to available device
        self.client.mySubscribe(self.crowdTopic)
        self.client.mySubscribe(self.ligthTopic)
        self.client.mySubscribe(self.statusTopic)

    def stop(self):
        self.workingStatus=False
        self.client.stop()
        # unregister device
        self.Reg.delete("service", self.serviceID)

    def notify(self, topic, msg):        
        payload=json.loads(msg)
        if topic == self.ligthTopic:
            zone = self.light2zone[payload["id"]]
            self.data[zone]["light"]=payload["brightness"]
        elif topic==self.crowdTopic:
            zones = payload["data"]
            for zone in set(zones.keys()):
                self.data[zone]["crowd"]=zones[zone]
        elif topic ==self.statusTopic:
            zones = payload["data"]
            for zone in set(zones.keys()):
                if zones[zone] == "open":
                    self.data[zone]["status"] = 1
                elif zones[zone] == "close":
                    self.data[zone]= 0
                else:
                    pass
        else:
            pass
        print(self.data)

    def thingSpeakUploader(self):
        while self.workingStatus:
            for key in list(self.tschannels.keys()):
                self.tschannels[key].UploadData(self.data[key]["crowd"],self.data[key]["light"],self.data[key]["status"])
                time.sleep(20)


if __name__ == "__main__":
    configFile = input("Enter the location of configuration file: ")
    if len(configFile) == 0:
        configFile = "./config.json"
    msgBroker= MsgBroker(configFile)
    t = threading.Thread(target=msgBroker.thingSpeakUploader)

    msgBroker.start()
    t.start()
    print("Camra control service running...")
    print("Enter 'q' to exit")
    while (True):
        if input() == 'q':
            break
    msgBroker.stop()