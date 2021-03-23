from common.MyMQTT import *
from common.RegManager import *
import json
import time


class cameraConnector():

    def __init__(self):
        try:
            self.conf = json.load(open(confAddr))
        except:
            print("Configuration file not found")
            exit()
        self.deviceId = self.conf["deviceId"]
        self.client = MyMQTT(self.deviceId, self.conf["broker"], int(self.conf["port"]), self)
        self.workingStatus = "on"

        self.cameraTopic = self.conf["cameraTopic"]
        self.switchTopic = self.conf["switchTopic"]
        self.__msg = {"cameraId":self.deviceId,"timestamp":"", "sequenceNum":0, "temperature":0}
        self.sequenceNum = 0

        regMsg = {"registerType": "device",
                  "id": self.deviceId,
                  "type": "camera",
                  "topic": self.cameraTopic,
                  "attribute": {"entranceId":self.conf ["entranceId"],
                                "motorControllerId":self.conf["motorControllerId"],
                                "RESTaddr":self.conf["RESTaddr"]}
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

    def publish(self,sequenceNum ,temp):
        msg = self.__msg
        msg["timestamp"] = str(time.time())
        msg["sequenceNum"] = sequenceNum
        msg["temperature"] = temp
        self.client.myPublish(self.cameraTopic, msg)
        print("Published: " + json.dumps(msg))

    def notify(self, topic, msg):
        data = json.load(msg)
        # ToDo: update process of input msg
        self.workingStatus = "on"
