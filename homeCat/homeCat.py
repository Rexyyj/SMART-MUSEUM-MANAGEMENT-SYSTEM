import cherrypy
import json


class HomeCat():
    exposed = True

    def __init__(self, configure):
        museum = json.load(open(configure))
        self.setting = museum
        self.devices = []
        self.services = []
        self.zones = museum['zones']
        self.entrances = museum['entrances']
        self.floor = museum["floors"]
        self.registerStatus = {"registerStatus": "Success", "errorType": "None","setting":""}
        self.getResult = {"status": "Success","failType":"None", "data": []}

    def PUT(self):
        body = cherrypy.request.body.read()
        data = json.loads(body)
        errorCode = self.checkRegister(data)
        if errorCode is not None:
            self.registerStatus["registerStatus"] = "Fail"
            self.registerStatus["errorType"] = errorCode
            self.registerStatus["setting"] = ""
            return json.dumps(self.registerStatus)

        if data['registerType'] == "device":
            self.devices.append(data)
        else:
            self.services.append(data)
        self.registerStatus["registerStatus"] = "Success"
        self.registerStatus["errorType"] = "None"
        self.registerStatus["setting"]=self.setting
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
                    self.getResult["status"] = "fail"
                    self.getResult["failType"]="No device registered"
                    self.getResult["data"] = []
                    return str(self.getResult)
                # select the specific type of devices
                searchDevice = []
                if uriLen == 1:
                    searchDevice = self.devices.copy()
                elif uriLen == 2:
                    for div in self.devices:
                        if div["type"] == uri[1]:
                            searchDevice.append(div)
                else:
                    self.getResult["status"] = "fail"
                    self.getResult["failType"]="uri invalid"
                    self.getResult["data"] = []
                    return str(self.getResult)
                # filter out the devices not in target if param exist
                if params != {}:
                    keys = params.keys()
                    existKeys = self.devices[0]["attribute"].keys()
                    if len(list(list(set(keys) - set(existKeys)))) != 0:
                        self.getResult["status"] = "fail"
                        self.getResult["failType"]="param not exist"
                        self.getResult["data"] = []
                        return str(self.getResult)
                    data = searchDevice.copy()
                    for key in keys:
                        for div in self.devices:
                            if div["attribute"][key] != params[key]:
                                try:
                                    data.remove(div)
                                except:
                                    pass
                    self.getResult["status"] = "success"
                    self.getResult["failType"]="None"
                    self.getResult["data"] = data
                    return json.dumps(self.getResult)
                else:
                    self.getResult["status"] = "success"
                    self.getResult["failType"]="None"
                    self.getResult["data"] = searchDevice
                    return json.dumps(self.getResult)

        # ToDo: add GET operation

    def DELETE(self):
        # ToDo: add DELETE operation
        pass

    def checkRegister(self, data):
        if data["registerType"] == "device":
            # check device id
            for div in self.devices:
                if div['id'] == data['id']:
                    return "Id already exist"
            # check device attributes
            try:
                self.floor.index(data["attribute"]["floor"])
                self.zones.index(data["attribute"]["enterZone"])
                self.zones.index(data["attribute"]["leavingZone"])
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


if __name__ == "__main__":
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tool.session.on': True
        }
    }
    cherrypy.config.update({'server.socket_port': 8090})
cherrypy.quickstart(HomeCat("./configuration.json"), '/', conf)
cherrypy.engine.start()
cherrypy.engine.block()
