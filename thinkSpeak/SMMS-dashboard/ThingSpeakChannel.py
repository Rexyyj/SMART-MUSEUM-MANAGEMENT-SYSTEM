import requests
import json
import paho.mqtt.publish as publish
import string
import random
import time

string.alphanum = '1234567890avcdefghijklmnopqrstuvwxyzxABCDEFGHIJKLMNOPQRSTUVWXYZ'

class TSchannel():
    def __init__(self,confAddr):
        try:
            self.AccountConf = json.load(open(confAddr))
        except:
            print("Configuration file not found")
            exit()

        self.URL = 'https://api.thingspeak.com/channels'
        self.MQTT_key = self.AccountConf["mqttAPIKey"]#"mqttAPIKey": "BGL8BLI28LL8MOKS",
        self.ChannelInfo = {}
        self.API_key = {"api_key": self.AccountConf["api_key"]}
        self.LastData = {}



    def CreateChannel(self, ChannelConf):
        try:
            self.conf = json.load(open(ChannelConf))
        except:
            print("Configuration file not found")
            exit()
        TSURL = self.URL + '.json'
        TSobj = self.conf
        Infotext = requests.post(TSURL, data = TSobj).text
        self.ChannelInfo = json.loads(Infotext)
        print(self.ChannelInfo)



    def UploadData(self,CrowdNumber,LightNumber):
        MQTT_broker = 'mqtt.thingspeak.com'
        writeAPIKey = self.ChannelInfo['api_keys'][0]['api_key']
        #while(1):
        clientID = ''
        # Create a random clientID.
        for x in range(1, 16):
            clientID += random.choice(string.alphanum)
        ChannelID = self.ChannelInfo['id']
        topic = "channels/" + str(ChannelID) + "/publish/" + str(writeAPIKey)
        payload = "field1=" + str(CrowdNumber) + "&field2=" + str(LightNumber)
        try:
            publish.single(topic, payload, hostname=MQTT_broker, transport='websockets', port=80, auth={'username': 'MQTT_publisher', 'password': self.MQTT_key})
            print("Trying to upload data Crowd = ", CrowdNumber, " Light = ", LightNumber, " to channel: ", ChannelID, " clientID= ", clientID)
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
        ChannelList = requests.get(listURL, data = self.API_key)
        return (ChannelList)

    def OutputList(self):
        ChannelList = self.GetChannelList().text
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
    X =Channel1.GetChannelList().text
    print(X)








