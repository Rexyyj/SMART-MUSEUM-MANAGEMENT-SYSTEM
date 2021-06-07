# -*- coding: utf-8 -*-
# @Time    : 3/31/2021 3:08 PM
# @Author  : Rex Yu
# @Mail    : jiafish@outlook.com
# @Github  : https://github.com/Rexyyj

import cherrypy
import json

from thinkSpeak.ThingSpeakChannel import TSchannel
import threading
import time

cherrypy_config_status = False


class HomeCat():
    exposed = True

    def __init__(self, configure, thingSpeakConf, use_exist_service = False):
        self.setting = json.load(open(configure))
        self.thingSpeakConf = json.load(open(thingSpeakConf))
        self.devices = []
        self.services = []
        self.registerStatus = {"status": "success",
                               "errorType": "None", "setting": ""}
        self.getResult = {"status": "Success", "failType": "None", "data": []}
        if use_exist_service ==True:
            exist_service = json.load(open("./thingSpeak_service.json"))
            channels = set([ch["name"] for ch in exist_service["attribute"]["channels"]])
            if channels != (set(self.setting["zones"].keys())-{"outdoor"}):
                raise ValueError(
                    "Exising thingSpeak service not conform with current museum!")
            else:
                self.services.append(exist_service)
                print(self.services)
        else:
            self.channels = []
            self.create_and_register_channels()

    def create_and_register_channels(self):
        print("creating channels...")
        zones = set(self.setting["zones"].keys())-{"outdoor"}
        channel_infos = []
        for zone in zones:
            channel = TSchannel(config=self.thingSpeakConf, channelName=zone)
            if channel.ChannelInfo != {}:
                channel_infos.append(channel.ChannelInfo)
                self.channels.append(channel)
            else:
                raise ValueError("Channel create fail...")
        reg = {
            "registerType": "service",
            "id": "thingspeak001",
            "type": "thingspeak",
            "attribute": {
                "config": self.thingSpeakConf,
                "channels": channel_infos
            }
        }
        self.services.append(reg)

    def set_getResult(self, status, failType, data):
        self.getResult["status"] = status
        self.getResult["failType"] = failType
        self.getResult["data"] = data

    def set_registerStatus(self, status, errorType, setting):
        self.registerStatus["status"] = status
        self.registerStatus["errorType"] = errorType
        self.registerStatus["setting"] = setting

    def POST(self):
        body = cherrypy.request.body.read()
        print(body)
        data = json.loads(body)
        errorCode = self.checkRegister(data)
        if errorCode is not None:
            self.set_registerStatus("fail", errorCode, "")
            return json.dumps(self.registerStatus)

        if data['registerType'] == "device":
            self.devices.append(data)
        else:
            self.services.append(data)
        self.set_registerStatus("success", "None", self.setting)
        json.dumps(self.registerStatus)
        return json.dumps(self.registerStatus)

    def GET(self, *uri, **params):
        uriLen = len(uri)
        if uriLen != 0:
            if uri[0] == "setting":
                return json.dumps(self.setting)
            elif uri[0] == "devices":
                # check the registered device list is empty or not
                if len(self.devices) == 0:
                    self.set_getResult("fail", "No such device registered", [])
                    return str(self.getResult)
                # select the specific type of devices
                searchDevice = []
                if uriLen == 1:
                    searchDevice = self.devices.copy()
                elif uriLen == 2:
                    for div in self.devices:
                        if div["type"] == uri[1]:
                            searchDevice.append(div)
                    if len(searchDevice) == 0:
                        self.set_getResult(
                            "fail", "No such device registered", [])
                        return str(self.getResult)
                else:
                    self.set_getResult("fail", "uri invalid", [])
                    return str(self.getResult)
                # filter out the devices not in target if param exist
                if params != {}:
                    keys = params.keys()
                    existKeys = searchDevice[0]["attribute"].keys()
                    if len(list(list(set(keys) - set(existKeys)))) != 0:
                        self.set_getResult("fail", "param not exist", [])
                        return str(self.getResult)
                    data = searchDevice.copy()
                    for key in keys:
                        for div in searchDevice:
                            if div["attribute"][key] != params[key]:
                                try:
                                    data.remove(div)
                                except:
                                    pass
                    self.set_getResult("success", "None", data)
                    return json.dumps(self.getResult)
                else:
                    self.set_getResult("success", "None", searchDevice)
                    return json.dumps(self.getResult)

            elif uri[0] == "service":
                if len(self.services) == 0:
                    self.set_getResult(
                        "fail", "No such service registered", [])
                    return str(self.getResult)
                searchService = []
                if uriLen == 1:
                    searchService = self.services.copy()
                elif uriLen == 2:
                    for ser in self.services:
                        if ser["type"] == uri[1]:
                            searchService.append(ser)
                    if len(searchService) == 0:
                        self.set_getResult(
                            "fail", "No such service registered", [])
                        return str(self.getResult)
                else:
                    self.set_getResult("fail", "uri invalid", [])
                    return str(self.getResult)
                self.set_getResult("success", "None", searchService)
                return json.dumps(self.getResult)

    def DELETE(self, *uri):
        if len(uri) == 2:
            if uri[0] == "device":
                for div in self.devices:
                    if div["id"] == uri[1]:
                        self.devices.remove(div)
                        break
            elif uri[0] == "service":
                # ToDo: add DELETE operation
                for ser in self.services:
                    if ser["id"] == uri[1]:
                        self.services.remove(ser)
                        break
                pass
            else:
                pass

    def checkRegister(self, data):
        if data["registerType"] == "device":
            # check device id
            for div in self.devices:
                if div['id'] == data['id']:
                    return "Id already exist"
            # check device attributes
            try:
                if data["type"] == "laser" or data["type"] == "motorController":
                    self.setting["floors"].index(data["attribute"]["floor"])
                    list(self.setting["zones"].keys()).index(
                        data["attribute"]["enterZone"])
                    list(self.setting["zones"].keys()).index(
                        data["attribute"]["leavingZone"])
                elif data["type"] == "camera":
                    self.setting["entrances"].index(
                        data["attribute"]["entranceId"])
                elif data["type"] == "lightController":
                    self.setting["floors"].index(data["attribute"]["floor"])
                    list(self.setting["zones"].keys()).index(
                        data["attribute"]["controlZone"])
                else:
                    pass
            except:
                return "Device attribute not valid"
        elif data["registerType"] == "service":
            # check service id
            for ser in self.services:
                if ser['id'] == data['id']:
                    return "Id already exist"
            # check device attributes
            try:
                # ToDo: add checking according service attribute
                pass
            except:
                return "Device attribute not valid"

    def destory_thinkSpeak_service(self):
        try:
            for channel in self.channels:
                channel.DeleteChannel()
                # control the request frequency
                time.sleep(5)
        except:
            print("Unable to delete channels...")

    def save_thingSpeak_service(self):
        # Assume currently we only have one thinkspeak service
        for ser in self.services:
            if ser["type"] == "thingspeak":
                with open('thingSpeak_service.json', 'w') as fp:
                    json.dump(ser, fp)
                break


def cherrypy_thread(homecat):
    global cherrypy_config_status
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tool.session.on': True
        }
    }
    # set this address to host ip address to enable dockers to use REST api
    host = input("ip address of homeCat: ")
    if len(host) == 0:
        host = "192.168.1.100"
    port = input("port of homeCat: ")
    if len(port) == 0:
        port = "8090"
    cherrypy.server.socket_host = host
    cherrypy.config.update(
        {'server.socket_port':int(port) })
    cherrypy_config_status = True
    print("Starting cherrypy engine...")
    print("Enter 'q' to exit\n")
    time.sleep(1)
    cherrypy.quickstart(homecat, '/', conf)


if __name__ == "__main__":
    print("Init homeCat...")
    if input("Use exist thingSpeak channel? [y/n]") == "n":
        mode =False
    else:
        mode = True
    homecat = HomeCat("./configuration.json", "./thingSpeakConfig.json",mode)

    print("Config homeCat address")
    t = threading.Thread(target=cherrypy_thread, args=(homecat,))
    t.start()
    # cherrypy.engine.block()
    while cherrypy_config_status == False:
        pass
    while True:
        if input() == "q":
            break
    if input("Save and keep thingSpeak channels? [y/n]") == "y":
        homecat.save_thingSpeak_service()
    else:
        homecat.destory_thinkSpeak_service()
    cherrypy.engine.exit()
