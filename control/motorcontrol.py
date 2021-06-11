# -*- coding: utf-8 -*-
"""
Created on Fri May  7 21:36:02 2021

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


 
    
class motorcontrol():
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
        self.__msg = {"id": self.clientID,
                      "timestamp": "","data":""}
        self.mapper = Mapper()
        # Register service to homeCat
        regMsg = {"registerType": "service",
                  "id": self.clientID,
                  "type": "motorcontrol",
                  "attribute": None}
        self.Reg = RegManager(self.homeCatAddr)
        self.museumSetting = self.Reg.register(regMsg)
        # check the register is correct or not
        if self.museumSetting == "":
            exit()
        #get all available light device from homeCat
        self.devices = self.Reg.getData("devices", "motor", None)["data"]
        # create a device id to zone map in format {"motor1":{"enterZone":"zone1","leavingZone":"zone2","currentStatus":close}}
        self.zone2motor=getMap_zone2device_LM(self,self.devices, self.museumSetting["zones"])
        self.motor2zone=getMap_device2zone_LM(self,self.devices)
        self.camera2motor=getMap_camera2motor_LM(self,self.devices)
        self.zones = {}
        for zoneDef in (set(self.museumSetting["zones"].keys())-{"outdoor"}):
            self.zones[zoneDef] = 0
            
            
        thingspeak = self.Reg.getData("service","thingspeak",None)["data"][0]
        channels = thingspeak["attribute"]["channels"]
        self.tschannels ={}
        for channel in channels:
            self.tschannels[channel["name"]] = TSchannel(config=thingspeak["attribute"]["config"],channelInfo=channel)
        print()  
        
    def publish(self,data):
        msg=self._msg
        msg["timestamp"]=str(datetime.datetime.now())
        msg["data"]=data
        self.client.myPublish(self.topic,msg)
        print("published:"+json.dumps(msg))
        
    def start(self):
        self.client.start()
        self.client.mySubscribe(self.conf["topicSub"])
        self.client.mySubscribe(self.conf["topicSub1"])
    def stop(self):
        self.client.stop()

    def notify(self,topic,msg):
        motorsatus={} #save the MotorID relating the zone
        message=json.loads(msg)
        if topic == "/Polito/iot/SMMS/museum01/overtempTopic":
           cameraID=message["cameraId"]
           motorwork={"motorID”:
                      "status"}
           motorwork['motorID']=self.camera2motor(cameraID)[0]
           Message={"id":motorwork[0],"timestamp":time.time(), "targetStatus":"close"}
           self.client.myPublish(self.topic,json.dumps(Message))
           time.sleep(10) #This time is that let unsafe people leaving 
           self.Message={"id":motorwork[0],"timestamp":time.time(), "targetStatus":"open"}
           self.client.myPublish(self.topic,json.dumps(Message))
           # Thie area I need a camera 2 motor.The register info include the camera relating motorcontrolID
        elif topic=="/Polito/iot/SMMS/museum01/crowdControl":
            zonepeoplenumber = message          #zone{zone1:"xx",zone2:"xx"....}
            overzone=[] # save the zone whose number is over limited number
            for zone in zonepeoplenumber.keys():
                if zonepeoplenumber[zone]>=50:
                    overzone.append(zone) # find wihcih zone is over overzone=[zone1,zone2,zone3]
            zone2motormap=self.zone2motor
            motor2zonemap=self.motor2zone
            for zone_motor in overzone:
                motorlist=zone2motormap[zone_motor]# motorlist={"zone1":["motor0","motor1"]}
                for motor in motorlist:
                    enterzone=motor2zonemap[motor]
                    if enterzone == zone_motor:
                        self.Message={"id":motor,"timestamp":time.time(), "targetStatus":"closed"}
                        self.client.myPublish(self.topic,json.dumps(Message))
                     

if __name__=="__main__":
    configFile = input("Enter the location of configuration file: ")
    if len(configFile) == 0:
        configFile = "./configs/motorcontrol.json"
    motorcontrol= motorcontrol(configFile)
    motorcontrol.start()
    print("motor control service running...")
    print("Enter 'q' to exit")
    while (True):
        if input() == 'q':
            break
    
    motorcontrol.stop()
