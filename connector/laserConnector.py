from MyMQTT import *
import requests
import json
import threading
import time


class LaserConnector():

    def __init__(self, confAddr):
        self.conf = json.load(open(confAddr))
        self.deviceId = self.conf["deviceId"]
        self.client = MyMQTT(self.deviceId, self.conf["broker"], self.conf["port"], None)
        self.switch = MyMQTT(self.deviceId, self.conf["broker"], self.conf["port"], self)
        self.workingStatus = "on"
        self.modeFlag = ""

        self.topic = self.conf["laserTopic"]
        self.__msg = {"laserId": self.deviceId, "timestamp": "", "in": 0, "out": 0}
        self.museumSetting = {}
        regMsg = {"registerType": "device",
                  "id": self.deviceId,
                  "type": "laser",
                  "topic": self.conf["topic"],
                  "attribute": {"floor": self.conf["floor"],
                                "enterZone": self.conf["enterZone"],
                                "leavingZone": self.conf["leavingZone"]}}
        if (self.register(self.conf["homeCatAddress"], regMsg)) == 0:
            exit()

    def register(self, homeCat, regMsg):
        reg = requests.put(homeCat, json.dumps(regMsg))
        response = json.load(reg)
        if response["status"] == "fail":
            print("Register Fail!!!")
            print("Fail type: " + response["errorType"])
            return 0
        else:
            print("Register Success")
            self.museumSetting = response["setting"]
            return 1

    def start(self):
        self.client.start()
        self.switch.start()

    def stop(self):
        self.client.stop()
        self.switch.stop()
        requests.delete(self.conf["homeCatAddress"] + "/laser/" + self.conf["deviceId"])

    def publish(self, inNum, outNum):
        msg = self.__msg
        msg["timestamp"] = str(time.time())
        msg["in"] = inNum
        msg["out"] = outNum
        self.client.myPublish(self.topic, msg)
        print("Published: " + json.dumps(msg))

    def notify(self, topic, msg):
        data = json.load(msg)
        # ToDo: update process of input msg
        self.workingStatus = "on"

    def manual(self):
        while self.modeFlag == "m":
            if self.workingStatus == "on":
                print("Press q to leave manual mode, or")
                print("Enter the number of people entering zone:" + self.conf["enterZone"])
                val1 = input()
                if val1 == "q":
                    break
                print("Enter the number of people leaving zone:" + self.conf["enterZone"])
                val2 = input()
                self.publish(val1, val2)
            else:
                time.sleep(1)

    def automatic(self):
        while self.modeFlag == "a":
            pass
        else:
            time.sleep(1)

    def modeReader(self):
        while True:
            if self.workingStatus != "m":
                self.modeFlag = input()


if __name__ == "__main__":
    laserConnector = LaserConnector("./laserConf.json")
    laserConnector.start()
    print("Please choose the working mode:")
    print("m: manual, a: automatic, q: quit")

    threads = []
    threads.append(threading.Thread(target=laserConnector.modeReader()))
    threads.append(threading.Thread(target=laserConnector.automatic()))
    threads.append(threading.Thread(target=laserConnector.manual()))

    for i in range(len(threads)):
        threads[i].start()

    while laserConnector.modeFlag != "q":
        time.sleep(1)

    laserConnector.stop()
