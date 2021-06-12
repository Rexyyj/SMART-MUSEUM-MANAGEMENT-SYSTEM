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
        self.broker = self.conf["broker"]
        self.client = MyMQTT(self.clientID, self.broker, self.port, self)
        self.crowdTopic = self.conf["topicSub"]
        self.camTopice = self.conf["topicSub1"]

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
        # get all available light device from homeCat
        self.motors = self.Reg.getData("devices", "motor", None)["data"]
        self.cameras = self.Reg.getData("devices", "camera", None)["data"]
        # create a device id to zone map in format {"motor1":{"enterZone":"zone1","leavingZone":"zone2","currentStatus":close}}
        self.zone2motor = self.mapper.getMap_zone2device_LM(
            self.motors, self.museumSetting["zones"])
        self.motor2zone = self.mapper.getMap_device2zone_LM(self.motors)
        self.camera2motor = self.mapper.getMap_camera2motor(self.cameras)
        self.zoneCapa =self.museumSetting["zones"]
        self.motor_status={}
        for motor in self.motors:
            self.motor_status[motor["id"]]={"current":"open","lock":"False"}


    def publish(self, id, status):
        msg = {"id": id, "timestamp": str(
            datetime.datetime.now()), "targetStatus": status}
        self.client.myPublish(self.topic, msg)
        print("published:"+json.dumps(msg))

    def start(self):
        self.client.start()
        self.client.mySubscribe(self.crowdTopic)
        self.client.mySubscribe(self.camTopice)

    def stop(self):
        self.client.stop()
        self.Reg.delete("service", self.clientID)

    def lock_reopen(self,motorId,s):
        time.sleep(s)
        self.publish(motorId, "open")
        self.motor_status[motorId]={"current":"open","lock":"False"}

    def notify(self, topic, msg):
        message = json.loads(msg)
        if topic == self.camTopice:
            cameraID = message["id"]
            motorId = self.camera2motor(cameraID)
            self.publish(motorId, "close")
            self.motor_status[motorId]={"current":"close","lock":"True"}
            t = threading.Thread(target=self.lock_reopen,args=(motorId,10,))
            t.start()
            # Thie area I need a camera 2 motor.The register info include the camera relating motorcontrolID
        elif topic == self.crowdTopic:
            zonepeoplenumber = message["data"]  # zone{zone1:"xx",zone2:"xx"....}
            overzone = []  # save the zone whose number is over limited number
            for zone in set(zonepeoplenumber.keys()):
                if int(zonepeoplenumber[zone]) >= int(self.zoneCapa[zone]):
                    # find wihcih zone is over overzone=[zone1,zone2,zone3]
                    overzone.append(zone)

            # Deal with zones with too much people
            for zone in overzone:
                # motorlist={"zone1":["motor0","motor1"]}
                motorlist = self.zone2motor[zone]
                for motor in motorlist:
                    if self.motor2zone[motor]["enterZone"] == zone:
                        if self.motor_status[motor]["current"]=="open" and self.motor_status[motor]["lock"]=="False":
                            self.publish(motor,"close")
                            self.motor_status[motor]={"current":"close","lock":"False"}
                        else:
                            pass
            # Deal with zones with people within capacity
            for zone in (set(self.zoneCapa.keys())-{"outdoor"}-overzone):
                motorlist = self.zone2motor[zone]
                for motor in motorlist:
                    if self.motor2zone[motor]["enterZone"] == zone:
                        if self.motor_status[motor]["current"]=="close" and self.motor_status[motor]["lock"]=="False":
                            self.publish(motor,"open")
                            self.motor_status[motor]={"current":"open","lock":"False"}
                        else:
                            pass


if __name__ == "__main__":
    configFile = input("Enter the location of configuration file: ")
    if len(configFile) == 0:
        configFile = "./configs/motorcontrol.json"
    motorcontrol = motorcontrol(configFile)
    motorcontrol.start()
    print("motor control service running...")
    print("Enter 'q' to exit")
    while (True):
        if input() == 'q':
            break

    motorcontrol.stop()
