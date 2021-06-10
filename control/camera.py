# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 21:13:28 2021

@author: DELL
"""


from common.RegManager import *
from common.MyMQTT import *
from common.Mapper import Mapper
import json
import datetime

class Camera():

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
                  "type": "camera",
                  "attribute": None
                  }
        self.Reg = RegManager(self.homeCatAddr)
        self.museumSetting = self.Reg.register(regMsg)
        # check the register is correct or not
        if self.museumSetting == "":
            exit()

        self.mapper = Mapper()
        # get all available laser device from homeCat
        self.devices = self.Reg.getData("devices", "camera", None)["data"]


    def publish(self,id,seq,temperature):
        msg=Message={"status":"danger",
                    "cameraId":id,
                    "sequenceNum":seq,
                    "timestamp":str(datetime.datetime.now()),
                    "temperature":temperature}

        self.client.myPublish(self.topic,msg)
        print("published:"+json.dumps(msg))
        
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

        
        payload=json.loads(msg)
        temperature=float(payload["temperature"])
        sequenceNum=payload["sequenceNum"]
        cameraID=payload["id"]
        if temperature >= 37:
            self.publish(cameraID,sequenceNum,temperature)
        else:
            pass


if __name__ == "__main__":
    configFile = input("Enter the location of configuration file: ")
    if len(configFile) == 0:
        configFile = "./configs/cameraControl.json"
    camera= Camera(configFile)
    camera.start()

    print("Camra control service running...")
    print("Enter 'q' to exit")
    while (True):
        if input() == 'q':
            break


    Camera.stop()