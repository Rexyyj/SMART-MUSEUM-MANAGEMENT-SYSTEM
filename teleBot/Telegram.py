from re import S
import time
from requests.sessions import merge_setting
import telepot
from telepot import Bot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from common.MyMQTT import MyMQTT
from common.RegManager import RegManager
from common.Mapper import Mapper
import datetime
import json
import requests
import time
import io


class Telegrambot():

    def __init__(self, confAddr):
        try:
            self.conf = json.load(open(confAddr))
        except:
            print("Configuration file not found")
            exit()
        self.token = self.conf["token"]
        self.bot = telepot.Bot(self.token)
        self.serviceId = self.conf["serviceId"]
        self.client = MyMQTT(
            self.serviceId, self.conf["broker"], int(self.conf["port"]), self)
        self.homeCatAddr = self.conf["homeCatAddress"]
        self.overtempTopic = self.conf["overTempTopic"]
        self.switchTopic = self.conf["switchTopic"]

        #self.__message = {"start": "", "info": ""}
        regMsg = {"registerType": "service",
                  "id": self.serviceId,
                  "type": "telegram",
                  "attribute": {"topic1": self.overtempTopic,
                                  "topic2": self.switchTopic,
                                }}
        self.Reg = RegManager(self.homeCatAddr)
        self.museumSetting = self.Reg.register(regMsg)
        # check the register is correct or not
        if self.museumSetting == "":
            exit()
        
        self.possibleSwitch =[]
        zones = set(self.museumSetting["zones"].keys())-{"outdoor"}
        for zone in zones:
            temp = [zone]
            self.possibleSwitch.append(temp)
        self.possibleSwitch.append(["All light"])
        self.possibleSwitch.append(["All laser"])
        self.possibleSwitch.append(["All motor"])
        self.possibleSwitch.append(["All camera"])
        self.possibleSwitch.append(["ALL"])

        self.mapper =Mapper()
        self.lights = self.Reg.getData("devices", "light", None)["data"]
        self.zone2light = self.mapper.getMap_zone2Light(self.lights,self.museumSetting["zones"])
        self.chat_auth = {}
        self.switchMode = "None"

    def start(self):
        self.client.start()
        # subscribe to topic according to available device
        self.client.mySubscribe(self.overtempTopic)
        MessageLoop(self.bot,self.msg_handler).run_as_thread()
        

    def stop(self):
        self.workingStatus = False
        self.client.stop()
        # unregister device
        self.Reg.delete("service", self.serviceID)

    def msg_handler(self,msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        message = msg['text']
        if message ==  "/start":
            self.initial_message(chat_id)
        elif message == "/client":
            self.user_message(chat_id)
        elif message == "/administrator":
            self.chat_auth[str(chat_id)]=False
            self.bot.sendMessage(chat_id, 'Please enter the password')
        elif message == "/see data":
            if self.check_auth(chat_id)==True:
                self.admin_see_data(chat_id)
            else:
                self.bot.sendMessage(chat_id, "Please send '/administrator' to login first!")
        elif message == "/operate":
            if self.check_auth(chat_id)==True:
                self.admin_operate(chat_id)
            else:
                self.bot.sendMessage(chat_id, "Please send '/administrator' to login first!")
        elif message == "/switchon":
            if self.check_auth(chat_id)==True:
                self.switchMode ="on"
                self.admin_switch_zone(chat_id)
            else:
                self.bot.sendMessage(chat_id, "Please send '/administrator' to login first!")
        elif message == "/switchoff":
            if self.check_auth(chat_id)==True:
                self.switchMode="off"
                self.admin_switch_zone(chat_id)
            else:
                self.bot.sendMessage(chat_id, "Please send '/administrator' to login first!")
        elif message == "/Logout":
            if self.check_auth(chat_id)==True:
                del self.chat_auth[str(chat_id)]
            else:
                self.bot.sendMessage(chat_id, "You haven't logged in!")
        else:
            if self.switchMode == "On" or self.switchMode=="Off":
                if self.check_auth(chat_id) ==True:
                    for switch in self.possibleSwitch:
                        if switch[0] == message:
                            self.admin_switch(chat_id,message,self.switchMode)
                            self.switchMode ="None"
                            self.bot.sendMessage(chat_id, "Command sent successfully!")
                            mark_up = ReplyKeyboardMarkup(keyboard=[['/operate'], ['/see data'],['/Logout']],one_time_keyboard=True)
                            self.bot.sendMessage(
                            chat_id, text='What would you like to do next?', reply_markup=mark_up)
                            return
                    self.bot.sendMessage(chat_id, 'Please enter the correct command!')
                else:
                    self.bot.sendMessage(chat_id, "Please send '/administrator' to login first!")
            else:
                try:
                    if self.chat_auth[str(chat_id)]==False:
                        if message == "admin":
                            self.chat_auth[str(chat_id)]=True
                            self.admin_message(chat_id)
                        else:
                            self.bot.sendMessage(chat_id, 'Password error! Please re-type password!')
                    else:
                        self.bot.sendMessage(chat_id, 'Please enter the correct command!')
                except:
                    self.bot.sendMessage(chat_id, "Please send '/administrator' to login !")

    def check_auth(self,chat_id):
        try:
            if self.chat_auth[str(chat_id)]==True:
                return True
            else:
                return False
        except:
            return False

    def initial_message(self,chat_id):
        # design as reply keyboard
        mark_up = ReplyKeyboardMarkup(keyboard=[['/client'], ['/administrator']],one_time_keyboard=True)
        self.bot.sendMessage(
            chat_id, text='Welcome to the museum!', reply_markup=mark_up)


    def user_message(self, chat_id):
        self.bot.sendMessage(chat_id,
                        parse_mode='Markdown',
                        text='*What do you want to know about the Museum?*'
                        )
        self.bot.sendMessage(chat_id,
                        parse_mode='Markdown',
                        text='[See historical data](https://thingspeak.com/channels/1334459)'
                        )
        self.bot.sendMessage(chat_id,
                        parse_mode='Markdown',
                        text='[See current number of people in each area](https://thingspeak.com/channels/1334459)'
                        )
    def admin_message(self,chat_id):
        mark_up = ReplyKeyboardMarkup(keyboard=[['/operate'], ['/see data']],one_time_keyboard=True)
        self.bot.sendMessage(
            chat_id, text='Login success! What would you like to do?', reply_markup=mark_up)


    def admin_see_data(self,chat_id):
        self.bot.keyboardRow = 2
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text='Historical data', url='https://thingspeak.com/channels/1334459')],
            [InlineKeyboardButton(
                text='Current number of people in each area', url='https://thingspeak.com/channels/1334459')],
            [InlineKeyboardButton(
                text='Total energy savings', url='https://thingspeak.com/channels/1334459')],
        ])
        self.bot.sendMessage(
        chat_id, 'What would you like to see?', reply_markup=keyboard)
        mark_up = ReplyKeyboardMarkup(keyboard=[['/operate'], ['/see data']],one_time_keyboard=True)
        self.bot.sendMessage(
            chat_id, text='What else would you like to do?', reply_markup=mark_up)

    def admin_operate(self, chat_id):
        mark_up = ReplyKeyboardMarkup(keyboard=[['/switchon'], ['/switchoff']],one_time_keyboard=True)
        self.bot.sendMessage(
            chat_id, text='Please select your operation...', reply_markup=mark_up)
    def admin_switch_zone(self,chat_id):
        mark_up = ReplyKeyboardMarkup(keyboard=self.possibleSwitch,
                                            one_time_keyboard=True)
        self.bot.sendMessage(
            chat_id, text='Please select the light in each zone or other devices you want to switch...', reply_markup=mark_up)

    def publish(self,target, switchTo):
        msg = {"target":target,"switchTo":switchTo,"timestamp":str(datetime.datetime.now())}
        self.client.myPublish(self.switchTopic, msg)
        print("Published: " + json.dumps(msg))

    def admin_switch(self,chat_id,message,switchMode):
        if message == "ALL":
            self.publish(target="ALL",switchTo=switchMode)
        elif message == "All light":
            self.publish(target="light",switchTo=switchMode)
        elif message == "All laser":
            self.publish(target="laser",switchTo=switchMode)
        elif message == "All motor":
            self.publish(target="motor",switchTo=switchMode)
        elif message == "All camera":
            self.publish(target="camera",switchTo=switchMode)
        else:
            lights = self.zone2light[message]
            for light in lights:
                self.publish(target=light,switchTo=switchMode)


    def sendImageRemoteFile(img_url):
        url = "https://api.telegram.org/bot<Token>/sendPhoto"
        remote_image = requests.get(img_url)
        photo = io.BytesIO(remote_image.content)
        photo.name = 'img.png'
        files = {'photo': photo}
        data = {'chat_id': "YOUR_CHAT_ID"}
        r = requests.post(url, files=files, data=data)
        print(r.status_code, r.reason, r.content)

    def notify(self, topic, msg):
        print (msg)
        # chat_id = update.message.chat.id
        # if topic == self.overtempTopic:
        #     with open('image.jpg', 'rb') as overtemperature_image:
        #         caption = "<a herf = 'https://>"
        #         bot = send_photo(
        #             chat_id,
        #             photo=overtemperature_image,
        #             caption=caption,
        #             parse_mode='HTML'
        #         )


if __name__ == "__main__":
    configFile = input("Enter the location of configuration file: ")
    if len(configFile) == 0:
        configFile = "./configuration.json"

    telegrambot = Telegrambot(configFile)
    telegrambot.start()
    

    print('waiting ...')

# Keep the program running.
    while 1:
        time.sleep(10)
