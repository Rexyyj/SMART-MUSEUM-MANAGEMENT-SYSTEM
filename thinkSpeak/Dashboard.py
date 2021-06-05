from ThingSpeakChannel import *
import requests
import ast
import time

class Dashboard():

	def __init__(self, ConfAddr):
		#self.AccountInfo = json.load(open(ConfAddr))
		self.UersInfo = TSchannel(ConfAddr)
		self.Num_of_Zones = len(self.UersInfo. GetChannelList().json())
		self.ChannelsInfo = self.UersInfo. GetChannelList().json()
		self.IDlist = []
		self.Namelist = []
		self.Crowdlist = []
		self.Lightlist = []
		self.TotalCrowd = 0
		for i in range (self.Num_of_Zones):
			self.Crowdlist.append(float(0))   #should be int
			self.Lightlist.append(float(0))

	def GetChannelsID(self):
		for i in range(self.Num_of_Zones):
			InfoStr = str(self.ChannelsInfo[i])
			DetailedInfo = ast.literal_eval(InfoStr)
			self.IDlist.append(str(DetailedInfo['id']))

	def GetChannelsNames(self):
		for i in range(self.Num_of_Zones):
			InfoStr = str(self.ChannelsInfo[i])
			DetailedInfo = ast.literal_eval(InfoStr)
			self.Namelist.append(DetailedInfo['name'])



	def GetLastData_ALL(self):

		for i in range (self.Num_of_Zones):
			ReadURL = 'https://api.thingspeak.com/channels' + '/' + self.IDlist[i] + '/feeds/last.json'  #
			Read_api = {"api_key": 'self.AccountConf["api_key"]'}  #
			ResponseData = requests.get(ReadURL, data=Read_api).json()
			self.Crowdlist[i] = float(ResponseData['field1'])  #should be integer
			self.Lightlist[i] = float(ResponseData['field2'])
		Crowd = 0
		for i in range (self.Num_of_Zones):
			Crowd += self.Crowdlist[i]
		self.TotalCrowd = Crowd



if __name__ == "__main__":
	test = Dashboard('Account.json')
	test.GetChannelsID()
	test.GetChannelsNames()
	print(test.Namelist)
	while True:
		test.GetLastData_ALL()

		print(test.Crowdlist)
		print(test.Lightlist)
		print(test.TotalCrowd)

		time.sleep(10)

