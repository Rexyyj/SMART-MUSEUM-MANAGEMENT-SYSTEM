from thinkSpeak.ThingSpeakChannel import TSchannel
import requests
import time
import ast
def main():
    TSinfo = TSchannel('Account.json')

    while (True):
        ChannelsInfo = TSinfo.GetChannelList().json()
        Num_of_Zones = len(ChannelsInfo)
        IDlist = []
        Namelist = []
        for i in range(Num_of_Zones):
            InfoStr = str(ChannelsInfo[i])
            DetailedInfo = ast.literal_eval(InfoStr)
            IDlist.append(str(DetailedInfo['id']))
            Namelist.append(str(DetailedInfo['name']))

        print(IDlist, Namelist)

        for i in range(Num_of_Zones):
            URL = 'https://api.thingspeak.com/channels/' + IDlist[i] + '/fields/1.csv'
            CS = requests.get(URL).text
            filename = Namelist[i] + '.csv'
            f = open(filename, "a")
            f.write(CS)
            f.close()

        time.sleep(5)

if __name__ == '__main__':
    main()





