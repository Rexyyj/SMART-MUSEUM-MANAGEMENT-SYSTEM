import os
import time
import json
from thinkSpeak.ThingSpeakChannel import TSchannel
import requests
import ast
import cherrypy
import threading
from pyspark import SparkConf, SparkContext
conf = SparkConf().setAppName("HOUR")
sc = SparkContext(conf=conf)


class Dashboard(object):
    exposed = True

    def __init__(self, ConfAddr):  # , ConfAddr
        # self.AccountInfo = json.load(open(ConfAddr))
        self.UersInfo = TSchannel(confAddr=ConfAddr)
        self.ChannelsInfo = json.loads(self.UersInfo.GetChannelList())
        self.Num_of_Zones = len(self.ChannelsInfo)
        self.IDlist = []
        self.Namelist = ['']*self.Num_of_Zones
        self.Crowdlist = [0]*self.Num_of_Zones
        self.Lightlist = [0]*self.Num_of_Zones
        self.Statuslist = [0] * self.Num_of_Zones
        self.TotalCrowd = 0
        self.STAdictlist = [None]*self.Num_of_Zones
        self.STAdictTotal = {}
        # for i in range (self.Num_of_Zones):
        # 	self.Crowdlist.append(int(0))
        # 	self.Lightlist.append(float(0))

    def GET(self, *path):
        # self.GetChannelsID()
        namelist = self.Namelist
        Total = self.GetLastData_ALL()
        data = self.Crowdlist
        Dict = {'Name': namelist, 'data': data}
        if len(path) != 0:
            if path[0] == 'current':
                Output = json.dumps(Dict)
                return Output
            elif path[0] == 'total':
                return str(Total)
            elif path[0] == 'historical':
                if path[1] == 'total':
                    time = list(self.STAdictTotal.keys())
                    number = list(self.STAdictTotal.values())
                    dict_total = {'name': time, 'data': number}
                    return json.dumps(dict_total)
                else:
                    for s in range(self.Num_of_Zones):
                        if path[1] == namelist[s]:
                            NAME = list(self.STAdictlist[s].keys())
                            VALUE = list(self.STAdictlist[s].values())
                            dict_sta = {'name': NAME, 'data': VALUE}
                            return json.dumps(dict_sta)
            elif path[0] == 'light':
                lightstatuslist = [{}]*self.Num_of_Zones
                for i in range(self.Num_of_Zones):
                    lightstatuslist[i] = {
                        "name": self.Namelist[i], "light": self.Lightlist[i]}
                return json.dumps(lightstatuslist)
            elif path[0] == 'status':
                zonestatuslist = [{}] * self.Num_of_Zones
                for i in range(self.Num_of_Zones):
                    if self.Statuslist[i] == 0:
                        ZoneStatus = 'CLOSE'
                    elif self.Statuslist[i] == 1:
                        ZoneStatus = 'OPEN'
                    zonestatuslist[i] = {"name": self.Namelist[i], "status": ZoneStatus}
                return json.dumps(zonestatuslist)

        else:
            return open("dashboard.html")

    def Statistic(self):

        while (True):
            self.Num_of_Zones = len(json.loads(self.UersInfo.GetChannelList()))
            self.GetChannelsID()
            self.GetChannelsNames()
            TotalRDD = sc.emptyRDD()
            for i in range(self.Num_of_Zones):
                filename = self.Namelist[i] + '.csv'
                rdd = sc.textFile(filename).map(lambda l: l.split(',')
                                  ).filter(lambda l: l[2] != 'field1')
                rddHour = rdd.map(lambda l: (l[0][11:13], (int(l[2]), 1)))
                rddSTA = rddHour.reduceByKey(lambda v1, v2: (v1[0] + v2[0], v1[1] + v2[1])).map(
                    lambda l: [l[0], int(l[1][0] / l[1][1])]).sortByKey()  # (time, number)

                TotalRDD = TotalRDD.union(rddSTA)
                STAdict = rddSTA.collectAsMap()
                self.STAdictlist[i] = STAdict

            STATotalRDD = TotalRDD.reduceByKey(lambda v1, v2: v1 + v2).sortByKey()
            self.STAdictTotal = STATotalRDD.collectAsMap()
            time.sleep(60)

    def GetChannelsID(self):
        for i in range(self.Num_of_Zones):
            InfoStr = str(self.ChannelsInfo[i])
            DetailedInfo = ast.literal_eval(InfoStr)
            self.IDlist.append(str(DetailedInfo['id']))

    def GetChannelsNames(self):
        for i in range(self.Num_of_Zones):
            InfoStr = str(self.ChannelsInfo[i])
            DetailedInfo = ast.literal_eval(InfoStr)
            self.Namelist[i] = DetailedInfo['name']

    def GetLastData_ALL(self):

        for i in range(self.Num_of_Zones):
            ReadURL = 'https://api.thingspeak.com/channels' + \
                '/' + self.IDlist[i] + '/feeds/last.json'  #
            Read_api = {"api_key": 'self.AccountConf["api_key"]'}  #
            ResponseData = requests.get(ReadURL, data=Read_api).json()
            self.Crowdlist[i] = int(ResponseData['field1'])  # should be integer
            self.Lightlist[i] = int(ResponseData['field2'])
            self.Statuslist[i] = int(ResponseData['field3'])
        Crowd = 0
        for i in range(self.Num_of_Zones):
            Crowd += self.Crowdlist[i]
        self.TotalCrowd = Crowd
        return self.TotalCrowd


if __name__ == "__main__":

    # multithreding, compute statistic data
    dashboard = Dashboard("./thingSpeakConfig.json")
    t = threading.Thread(target=dashboard.Statistic)
    t.start()

    conf = {
        '/': {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                'tools.staticdir.root': os.path.abspath(os.getcwd()),
            },
         '/assets': {
         'tools.staticdir.on': True,
         'tools.staticdir.dir': './assets'
         },
    }

    cherrypy.tree.mount(dashboard, '/', conf)
    cherrypy.server.socket_host = "192.168.1.101"
    cherrypy.config.update({'server.socket_port': 8090})
    cherrypy.engine.start()
    cherrypy.engine.block()




