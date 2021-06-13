import time
import telepot
from telepot import Bot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from common.MyMQTT import MyMQTT
from common.RegManager import RegManager
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

    def start(self):
        self.client.start()
        # subscribe to topic according to available device
        self.client.mySubscribe(self.overtempTopic)
        # Add user message???
        MessageLoop(self.bot).run_as_thread()

    def stop(self):
        self.workingStatus = False
        self.client.stop()
        # unregister device
        self.Reg.delete("service", self.serviceID)

    def initial_message(self,msg):
        # design as reply keyboard
        content_type, chat_type, chat_id = telepot.glance(msg)
        #self.chatIDs.append(chat_ID)
        message = msg['text']
        if msg['text'] == '/start':
            mark_up = ReplyKeyboardMarkup(keyboard=[['/Client'], ['/Administrator']],one_time_keyboard=True)
            self.bot.sendMessage(
                chat_id, text='Welcome to the museum!', reply_markup=mark_up)
        else:
            self.bot.sendMessage(chat_id, 'Please enter the correct command!')

    def user_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        print(content_type, chat_type, chat_id)
        message = msg['text']
        if msg['text'] == '/client':
            self.bot.sendMessage(chat_id,
                            parse_mode='Markdown',
                            text='*What do you want to know about the Museum?*/n [historical data](https://thingspeak.com/channels/1334459)/n[Current number of people in each area](https://thingspeak.com/channels/1334459)'
                            )

        elif msg['text'] == '/Administrator':
            self.bot.sendMessage(chat_id, 'Please enter the password')
            # authentication   URL button callback=url
            if msg['text'] == 'password':
                self.bot.keyboardRow = 2
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(
                        text='historical data', url='https://thingspeak.com/channels/1334459')],
                    [InlineKeyboardButton(
                        text='"Current number of people in each area"', url='https://thingspeak.com/channels/1334459')],
                    [InlineKeyboardButton(
                        text='Total energy savings', url='https://thingspeak.com/channels/1334459')],
                ])
                self.bot.sendMessage(
                    chat_id, 'What would you like to do?', reply_markup=keyboard)
                mark_up = ReplyKeyboardMarkup(keyboard=[['zoneA'], ['zoneB'], ['zoneC'], ['zoneD']],
                                                  one_time_keyboard=True)
                if msg['text'] == '/switchoff':
                    payload = self.__message.copy()
                    payload['e'][0]['v'] = "off"
                    payload['e'][0]['t'] = time.time()
                    self.client.myPublish(
                        self.switchTopic, self.lightTopic, payload)
                    self.bot.sendMessage(
                        chat_id, text='What light would you like to turn off?', reply_markup=mark_up)
                elif msg['text'] == '/switchon':
                    payload = self.__message.copy()
                    payload['e'][0]['v'] = "on"
                    payload['e'][0]['t'] = time.time()
                    self.client.myPublish(
                        self.switchTopic, self.lightTopic, payload)
                    self.bot.sendMessage(
                        chat_id, text='turn on all the lights', reply_markup=mark_up)
            else:
                self.bot.sendMessage(chat_id, 'Please enter correct password')

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

    telegrambto = Telegrambot(configFile)
    telegrambto.start()

    print('waiting ...')

# Keep the program running.
    while 1:
        time.sleep(10)
