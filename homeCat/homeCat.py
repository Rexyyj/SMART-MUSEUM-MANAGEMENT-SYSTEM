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
        errorCode = ""
        errorCode = self.checkRegister(data)
        if errorCode != "":
            self.registerStatus["registerStatus"] = "Fail"
            self.registerStatus["errorType"] = errorCode
            return json.dump(self.registerStatus)

        if data['registerType'] == "device":
            self.devices.append(data)
        else:
            self.services.append(data)
        self.registerStatus["registerStatus"] = "Success"
        self.registerStatus["errorCode"] = "None"
        return json.dump(self.registerStatus)

    def GET(self, *uri, **params):
        pass

    def DELETE(self):
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


if __name__ == "__main__":
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tool.session.on': True
        }
    }

cherrypy.quickstart(HomeCat("./configuration.json"), '/', conf)
cherrypy.engine.start()
cherrypy.engine.block()
