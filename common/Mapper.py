

class Mapper():
    def __init__(self):
        pass

    # raw device: devices list with zone information in attribute
    # raw zones: zone:capa dict like this {"zone1":50,"zone2":1000}
    # raw entrance : list of entrance ["entrance1","entrance2"]
    def getMap_device2zone_LM(self,raw_devices):
        device2zone = {} 
        for dev in raw_devices:
            zones = {"enterZone": dev["attribute"]["enterZone"], "leavingZone": dev["attribute"]["leavingZone"]}
            device2zone[dev["id"]] = zones
        return device2zone # Format: {"laser001":{"enterZone":"zone1","leavingZone":"zone2"}}

    def getMap_light2zone(self,raw_device):
        light2zone ={} 
        for light in raw_device:
            light2zone[light["id"]]=light["attribute"]["controlZone"]
        return light2zone # Format: {"light01":"zone1"}

    def getMap_camera2entrance(self,raw_device):
        cam2ent ={} 
        for cam in raw_device:
            cam2ent[cam["id"]]=cam["attribute"]["entranceId"]
        return cam2ent #Format: {"camera01":"zone1"}

    def getMap_zone2device_LM(self,raw_device,raw_zones):
        zone2dev ={} 
        for zone in (set(raw_zones.keys())-{"outdoor"}):
            devs =set()
            for device in raw_device:
                if device["attribute"]["enterZone"]==zone or device["attribute"]["leavingZone"]==zone:
                    devs.add(device["id"])
            zone2dev[zone]=devs
        return zone2dev # Format: {"zone1":["laser001","laser002"]}


    def getMap_zone2Light(self,raw_device,raw_zones):
        zone2light ={} 
        for zone in (set(raw_zones.keys())-{"outdoor"}):
            lig =set()
            for device in raw_device:
                if device["attribute"]["controlZone"]==zone:
                    lig.add(device["id"])
            zone2light[zone]=lig
        return zone2light # Format: {"zone1":["light001","light002"]}

    def getMap_entrance2camera(self,raw_device,raw_entrance):
        ent2cam ={} 
        for ent in raw_entrance:
            cam = set()
            for device in raw_device:
                if device["entranceId"]==ent:
                    cam.add(device["id"])
            ent2cam[ent]=cam
        return ent2cam # Format: {"entrance1":["camera001","camera002"]}