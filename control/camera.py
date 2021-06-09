# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 21:13:28 2021

@author: DELL
"""


from common.RegManager import *
from common.MyMQTT import *
from common.Mapper import Mapper
import json
import time
import requests
import threading
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
        self.topic = self.conf["topic"]
        self.broker = self.conf["broker"]
        self.client = MyMQTT(self.clientID, self.broker, self.port, self)
        # Register service to homeCat
        regMsg = {"registerType": "service",
                  "id": self.clientID,
                  "type": "camera",
                  "attribute": None}
        self.Reg = RegManager(self.homeCatAddr)
        self.museumSetting = self.Reg.register(regMsg)
        # check the register is correct or not
        if self.museumSetting == "":
            exit()

        self.mapper = Mapper()
        # get all available laser device from homeCat
        self.devices = self.Reg.getData("devices", "camera", None)["data"]
        # create thingspeak instances
        #thingspeak = self.Reg.getData("service","thingspeak",None)["data"][0]
        #channels = thingspeak["attribute"]["channels"]
        #self.tschannels ={}
        #for channel in channels:
            #self.tschannels[channel["name"]] = TSchannel(config=thingspeak["attribute"]["config"],channelInfo=channel)

    def publish(self,data):
        msg=self._msg
        msg["timestamp"]=str(datetime.datetime.now())
        msg["data"]=data
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

        
        temperature_conditon=json.loads(msg)
        temperature=int(temperature_conditon["temperature"])
        sequenceNum=temperature_conditon["sequenceNum"]
        cameraID=temperature["cameraID"]
        if temperature >= 37:
            Message={"status":"danger","cameraId":cameraID,"sequenceNum":sequenceNum,"timestamp":time.time(),"temperature":temperature}
            self.client.myPublish("/Polito/iot/SMMS/museum01/overtempTopic",json.dumps(Message))
            data=Message
            camera.publish(data)
        else:
            pass




        print("Received: " + json.dumps(temperature_conditon, indent=4))
        print("Processed: " + json.dumps(Message, indent=4))

        
        # 传输topic需要跟thinkspeak


if __name__ == "__main__":
    #configFile = input("Enter the location of configuration file: ")
    #if len(configFile) == 0:
    configFile = "./configs/CameraControl"
    camera= Camera(configFile)
    #t = threading.Thread(target=customermanager.thingSpeakUploader)
    camera.start()
    #t.start()
    print("Camra control service running...")
    print("Enter 'q' to exit")
    while (True):
        if input() == 'q':
            break


    Camera.stop()