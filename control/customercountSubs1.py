# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 16:45:30 2021

@author: Administrator
"""

from RegManager import *
from MyMQTT import *
import json
import time
import requests


class Customermanager():

    def __init__(self, clientID, topic, broker, port):
        self.homeCatAddr = "http://192.168.1.100:8090"
        self.clientID = clientID
        self.port = port
        self.topic = topic
        self.broker = broker
        self.client = MyMQTT(clientID, self.broker, self.port, self)
        # Register service to homeCat
        regMsg = {"registerType": "service",
                  "id": self.clientID,
                  "type": "laser",
                  "attribute": {}}
        self.Reg = RegManager(self.homeCatAddr)
        self.museumSetting = self.Reg.register(regMsg)
        # check the register is correct or not
        if self.museumSetting == "":
            exit()
        # get all available laser device from homeCat
        self.devices = self.Reg.getData("devices", "laser", None)["data"]
        # create a device id to zone map in format {"laser1":{"enterZone":"zone1","leavingZone":"zone2"}}
        self.device2zone = {}
        for dev in self.devices:
            zones = {"enterZone": dev["attribute"]["enterZone"], "leavingZone": dev["attribute"]["leavingZone"]}
            self.device2zone[dev["id"]] = zones
        # define zone counter from museum setting
        self.zone = {}
        for zoneDef in self.museumSetting["zones"]:
            self.zone[zoneDef] = 20


    def start(self):
        self.client.start()
        # subscribe to topic according to available device
        for dev in self.devices:
            self.client.mySubscribe(dev["topic"])

    def stop(self):
        self.client.stop()
        # unregister device
        self.Reg.delete("service", self.clientID)

    def notify(self, topic, msg):

        payload = json.loads(msg)

        laserID = payload["laserID"]
        # add int due to joson only transmit string,can not do +- calculation
        enter = int(payload['enter'])
        leaving = int(payload['leaving'])


        self.zone[self.device2zone[laserID]["enterZone"]] += enter
        if (self.zone[self.device2zone[laserID]["leavingZone"]] - leaving) > 0:
            self.zone[self.device2zone[laserID]["leavingZone"]] -= leaving
        else:
            self.zone[self.device2zone[laserID]["leavingZone"]] = 0

        # if laserID == "laser0":
        #     self.zone['zone1'] += enter
        #     self.zone['zone1'] -= leaving
        # elif laserID == "laser1":
        #     self.zone['zone2'] += enter
        #     self.zone['zone2'] -= leaving
        #     self.zone['zone1'] -= enter
        #     self.zone['zone1'] += leaving
        # elif laserID == "laser2":
        #     self.zone['zone3'] += enter
        #     self.zone['zone3'] -= leaving
        #     self.zone['zone2'] -= enter
        #     self.zone['zone2'] += leaving
        # elif laserID == "laser3":
        #     self.zone['zone4'] += enter
        #     self.zone['zone4'] -= leaving
        #     self.zone['zone3'] -= enter
        #     self.zone['zone3'] += leaving
        # else:
        #     pass

        print("Received: " + json.dumps(payload, indent=4))
        print("Processed: " + json.dumps(self.zone, indent=4))

        self.client.myPublish("yourtopic", json.dumps(self.zone))
        # 传输topic需要跟thinkspeak


if __name__ == "__main__":
    # manager=RegManager('http://localhost:8090/')
    # getdata=manager.getData('devices','type','floor=2&enterZone=zone1')
    # topic = getdata["topic"]
    port = 1883
    topic = '/Polito/iot/SMMS/museum01/floor1/gate1/laser'
    broker = 'localhost'  # 其他人运行时请修改broker
    yourtest = Customermanager("CustormerNumber", topic, broker, port)

    yourtest.start()

    while (True):
        pass
