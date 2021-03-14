import cherrypy
import json


class HomeCat():
    exposed = True

    def __init__(self, configure):
        museum = json.load(open(configure))
        self.devices = []
        self.services = []
        self.zones = museum['zones']
        self.entrances = museum['entrances']
        self.floor = museum["floors"]
        self.registerStatus = {"registerStatus": "Success", "errorType": "None"}
        pass

    def PUT(self):
        body = cherrypy.request.body.read()
        data = json.loads(body)
        errorCode = self.checkRegister(data)
        if errorCode is not None:
            print("inError")
            self.registerStatus["registerStatus"] = "Fail"
            self.registerStatus["errorType"] = errorCode
            return json.dumps(self.registerStatus)

        if data['registerType'] == "device":
            self.devices.append(data)
        else:
            self.services.append(data)
        self.registerStatus["registerStatus"] = "Success"
        self.registerStatus["errorType"] = "None"
        print("in here")
        json.dumps(self.registerStatus)
        return json.dumps(self.registerStatus)

    def GET(self, *uri, **params):
        # ToDo: add GET operation
        pass

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
                print("pass here")
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
    cherrypy.config.update({'server.socket_port':8090})
cherrypy.quickstart(HomeCat("./configuration.json"), '/', conf)
cherrypy.engine.start()
cherrypy.engine.block()
