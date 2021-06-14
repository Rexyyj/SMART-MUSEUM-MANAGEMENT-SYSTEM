# -*- coding: utf-8 -*-
# @Time    : 3/31/2021 3:08 PM
# @Author  : Rex Yu
# @Mail    : jiafish@outlook.com
# @Github  : https://github.com/Rexyyj

from common.MyMQTT import *
from common.RegManager import *
import json
import time


class MotorConnector():

    def __init__(self, confAddr):
        try:
            self.conf = json.load(open(confAddr))
        except:
            print("Configuration file not found")
            exit()
        self.deviceId = self.conf["deviceId"]
        self.client = MyMQTT(self.deviceId, self.conf["broker"], int(self.conf["port"]), self)
        self.workingStatus = "on"
        self.doorStatus = "close"
        self.motorTopic = self.conf["motorTopic"]
        self.switchTopic = self.conf["switchTopic"]

        regMsg = {"registerType": "device",
                  "id": self.deviceId,
                  "type": "motor",
                  "topic": self.motorTopic,
                  "attribute": {"floor": self.conf["floor"],
                                "enterZone": self.conf["enterZone"],
                                "leavingZone": self.conf["leavingZone"],
                                "entranceId":self.conf["entrance"],
                                "currentStatus": self.doorStatus}
                  }
        self.Reg = RegManager(self.conf["homeCatAddress"])
        self.museumSetting = self.Reg.register(regMsg)
        if self.museumSetting == "":
            exit()

    def start(self):
        self.client.start()
        self.client.mySubscribe(self.switchTopic)
        self.client.mySubscribe(self.motorTopic)

    def stop(self):
        self.client.stop()
        self.Reg.delete("device", self.conf["deviceId"])

    def notify(self, topic, msg):
        data = json.loads(msg)
        if topic == self.switchTopic:
            if data["target"]=="ALL" or data["target"]=="motor" or data["target"]==self.deviceId:
                self.workingStatus = data["switchTo"]
                print(str(self.deviceId)+" switch to "+data["switchTo"])
        elif topic == self.motorTopic:
            if self.workingStatus=="on":
                targetStatus = data["targetStatus"]
                self.setDoorStatus(targetStatus)
            else:
                pass

    def setDoorStatus(self, status):
        self.doorStatus = status
        time.sleep(1)
        print("Door " + self.deviceId + " status:" + self.doorStatus)


if __name__ == "__main__":
    configFile = input("Enter the location of configuration file: ")
    if len(configFile) == 0:
        configFile = "./configs/motorConfig.json"
    motorConnector = MotorConnector(configFile)
    motorConnector.start()
    print("Motor connector is running...")

    while True:
        c = input("Enter q if want to stop motor connector")
        if c == "q":
            break

    motorConnector.stop()
