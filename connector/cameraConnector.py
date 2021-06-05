# -*- coding: utf-8 -*-
# @Time    : 3/31/2021 3:08 PM
# @Author  : Rex Yu
# @Mail    : jiafish@outlook.com
# @Github  : https://github.com/Rexyyj

from common.MyMQTT import *
from common.RegManager import *
from random import seed
from random import randint
from random import gauss
import json
import time
import cv2


class CameraConnector():

    def __init__(self, confAddr):
        try:
            self.conf = json.load(open(confAddr))
        except:
            print("Configuration file not found")
            exit()
        self.confAddr = confAddr
        self.deviceId = self.conf["deviceId"]
        self.client = MyMQTT(self.deviceId, self.conf["broker"], int(self.conf["port"]), self)
        self.workingStatus = "on"

        self.cameraTopic = self.conf["cameraTopic"]
        self.switchTopic = self.conf["switchTopic"]
        self.__msg = {"id": self.deviceId, "timestamp": "", "sequenceNum": 0, "temperature": 0}
        self.sequenceNum = 0

        seed(1)

        regMsg = {"registerType": "device",
                  "id": self.deviceId,
                  "type": "camera",
                  "topic": self.cameraTopic,
                  "attribute": {"entranceId": self.conf["entranceId"],
                                "motorControllerId": self.conf["motorControllerId"],
                                "RESTaddr": self.conf["RESTaddr"]}
                  }
        self.Reg = RegManager(self.conf["homeCatAddress"])
        self.museumSetting = self.Reg.register(regMsg)
        if self.museumSetting == "":
            exit()

    def start(self):
        self.client.start()
        self.client.mySubscribe(self.switchTopic)

    def stop(self):
        self.client.stop()
        self.Reg.delete("device", self.conf["deviceId"])

    def publish(self, sequenceNum, temp):
        msg = self.__msg
        msg["timestamp"] = str(time.time())
        msg["sequenceNum"] = sequenceNum
        msg["temperature"] = temp
        self.client.myPublish(self.cameraTopic, msg)
        print("Published: " + json.dumps(msg))

    def notify(self, topic, msg):
        data = json.loads(msg)
        print(json.dumps(data))
        # ToDo: update process of input msg
        self.workingStatus = "on"

    def replay(self):
        while True:
            record = input("Input the record file: ")
            try:
                datas = json.load(open(record))
            except:
                print("The record file not exist!")
                continue
            for data in datas["data"]:
                self.publish(data["sequence"], data["temp"])
                time.sleep(5)
            option = input("Input r: replay, q: quit\n")
            if option == "r":
                continue
            else:
                break

    def automatic(self):
        rawNum = randint(1, 2)
        print("Use ctrl+c to terminate automatic message generation")
        try:
            while True:
                self.sequenceNum = self.sequenceNum + 1

                temp = format(gauss(36.7, 1.3),'.2f')

                rawImg = cv2.imread(self.conf["rawImgAddress"] + str(rawNum) + ".png")
                rawImg = cv2.resize(rawImg, (480, 640), interpolation=cv2.INTER_AREA)
                generatedImg = cv2.rectangle(rawImg, (80, 450), (400, 50), (0, 255, 0), 2)
                generatedImg = cv2.putText(generatedImg, str(temp), (210, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),
                                           2, cv2.LINE_AA)
                cv2.imwrite(self.conf["storeImgAddress"] + str(self.sequenceNum) + ".jpg", generatedImg)

                self.publish(self.sequenceNum,temp)

                time.sleep(5)
        except:
            pass


if __name__ == "__main__":
    configFile = input("Enter the location of configuration file: ")
    if len(configFile) == 0:
        configFile = "./configs/cameraConfig.json"
    cameraConnector = CameraConnector(configFile)

    cameraConnector.start()
    time.sleep(1)

    while True:
        print("Please choose the working mode:")
        print("r: replay, a: automatic q: quit")
        mode = input()
        if mode == "q":
            break
        elif mode == "r":
            cameraConnector.replay()
        elif mode == "a":
            cameraConnector.automatic()

    cameraConnector.stop()
