

class Mapper():
    def __init__(self) -> None:
        pass

    # raw device: devices list with zone information in attribute
    # raw zones: zone:capa dict like this {"zone1":50,"zone2":1000}
    # raw entrance : list of entrance ["entrance1","entrance2"]
    def getMap_device2zone_LM(self, raw_devices) -> dict:
        device2zone = {}
        for dev in raw_devices:
            zones = {"enterZone": dev["attribute"]["enterZone"],
                     "leavingZone": dev["attribute"]["leavingZone"]}
            device2zone[dev["id"]] = zones
        # Format: {"laser001":{"enterZone":"zone1","leavingZone":"zone2"}}
        return device2zone

    def getMap_light2zone(self, raw_device) -> dict:
        light2zone = {}
        for light in raw_device:
            light2zone[light["id"]] = light["attribute"]["controlZone"]
        return light2zone  # Format: {"light01":"zone1"}

    def getMap_camera2entrance(self, raw_device)-> dict:
        cam2ent = {}
        for cam in raw_device:
            cam2ent[cam["id"]] = cam["attribute"]["entranceId"]
        return cam2ent  # Format: {"camera01":"zone1"}

    def getMap_motor2entrance(self,raw_device) ->dict:
        motor2entrance ={}
        for dev in raw_device:
            motor2entrance[dev["id"]]=dev["attribute"]["entrance"]
        return motor2entrance # Format: {"motor0":"Entrance0"}

    def getMap_zone2device_LM(self, raw_device, raw_zones) -> dict:
        zone2dev = {}
        for zone in (set(raw_zones.keys())-{"outdoor"}):
            devs = set()
            for device in raw_device:
                if device["attribute"]["enterZone"] == zone or device["attribute"]["leavingZone"] == zone:
                    devs.add(device["id"])
            zone2dev[zone] = list(devs)
        return zone2dev  # Format: {"zone1":["laser001","laser002"]}

    def getMap_zone2Light(self, raw_device, raw_zones)-> dict:
        zone2light = {}
        for zone in (set(raw_zones.keys())-{"outdoor"}):
            lig = set()
            for device in raw_device:
                if device["attribute"]["controlZone"] == zone:
                    lig.add(device["id"])
            zone2light[zone] = list(lig)
        return zone2light  # Format: {"zone1":["light001","light002"]}

    def getMap_entrance2camera(self, raw_device, raw_entrance)-> dict:
        ent2cam = {}
        for ent in raw_entrance:
            cam = set()
            for device in raw_device:
                if device["entranceId"] == ent:
                    cam.add(device["id"])
            ent2cam[ent] = list(cam)
        return ent2cam  # Format: {"entrance1":["camera001","camera002"]}

    def getMap_entrance2motor(self, raw_device, raw_entrance):
        ent2mot={}
        for ent in raw_entrance:
            mot =set()
            for dev in raw_device:
                if dev["entranceId"] == ent:
                    mot.add(dev["id"])
            ent2mot[ent]=list(mot)
        return ent2mot # Format: {"entrance1":["motor001","motor002"]}
