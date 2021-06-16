import requests
import json
import paho.mqtt.publish as publish
import string
import random
import time

string.alphanum = '1234567890avcdefghijklmnopqrstuvwxyzxABCDEFGHIJKLMNOPQRSTUVWXYZ'

class TSchannel():
    def __init__(self,confAddr=None,config=None,channelName=None,channelInfo=None):
        if confAddr!=None:
            try:
                self.config = json.load(open(confAddr))
            except:
                print("Configuration file not found")
                exit()

            self.URL = self.config["URL"]
            self.MQTT_key = self.config["mqttAPIKey"]#"mqttAPIKey": "BGL8BLI28LL8MOKS",
            self.ChannelInfo = {}
            self.API_key = {"api_key": self.config["api_key"]}
            self.LastData = {}
            self.clientID = ''
            # Create a random clientID.
            for x in range(1, 16):
                self.clientID += random.choice(string.alphanum)
        elif config!=None and channelName!=None:
            self.ChannelInfo = {}
            self.config = config
            self.URL = self.config["URL"]
            self.MQTT_key = self.config["mqttAPIKey"]
            self.API_key = {"api_key": self.config["api_key"]}
            self.CreateChannel(channelName)
        elif config!=None and channelInfo!=None:
            self.ChannelInfo = channelInfo
            self.config = config
            self.URL = self.config["URL"]
            self.MQTT_key = self.config["mqttAPIKey"]
            self.API_key = {"api_key": self.config["api_key"]}
        else:
            raise ValueError


    def CreateChannel(self,name):
        TSURL = self.URL + '.json'
        TSobj ={
            "api_key": self.config["api_key"],
            "name": name,
            "public_flag": self.config["public_flag"],
            "field1": self.config["field1"],
            "field2": self.config["field2"],
            "field3": self.config["field3"]
        }
        Infotext = requests.post(TSURL, data = TSobj).text
        self.ChannelInfo = json.loads(Infotext)
        print(self.ChannelInfo)


    # target could be crowd / light
    def UploadData(self,crowdNum,lightNum,zoneStatus):
        MQTT_broker = 'mqtt.thingspeak.com'
        writeAPIKey = self.ChannelInfo['api_keys'][0]['api_key']

        ChannelID = self.ChannelInfo['id']
        topic = "channels/" + str(ChannelID) + "/publish/" + str(writeAPIKey)
        payload = "field1=" + str(crowdNum) + "&field2=" + str(lightNum) +"&field3=" + str(zoneStatus)
        try:
            print("Sending msg to thingSpeak...")
            publish.single(topic, payload, hostname=MQTT_broker, transport='websockets', port=80, auth={'username': 'MQTT_publisher', 'password': self.MQTT_key})
            #print("Trying to upload data to ", target, " value = ", str(value), " to channel: ", str(ChannelID), " clientID= ", str(self.clientID))
        except:
            print("There was an error while publishing the data.")




    def DeleteChannel(self):
        channelURL = self.URL + '/' + str(self.ChannelInfo['id'])
        Deleted = requests.delete(channelURL, data = self.API_key).text

        if ('!DOCTYPE html' in Deleted):
            print("Error! You can try to delete manually. ")
        else:
            print("Successfully deleted! Deleted channel info:")
            print(Deleted)



    def GetChannelList(self):
        listURL = self.URL + '.json'
        ChannelList = requests.get(listURL, data = self.API_key).text
        print(ChannelList)



    def GetLastData(self):
        ReadURL = self.URL + '/' + self.ChannelInfo['id'] + '/feeds/last.json'#
        Read_api = {"api_key": 'self.AccountConf["api_key"]'}#
        ResponseData = requests.get(ReadURL, data = Read_api).text
        self.LastData = json.loads(ResponseData)



    def CurrentCrowd(self):
        self.GetLastData()
        return self.LastData['field1']

    def CurrentLight(self):
        self.GetLastData()
        return self.LastData['field2']



if __name__ == "__main__":

    Channel1 = TSchannel('Account.json')
    Channel1.CreateChannel('testchannel.json')
    while True:
        x = random.randint(1, 10)
        y = random.randint(1,10)
        Channel1.UploadData(x,y)
        time.sleep(20)











