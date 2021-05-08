Services (Using PUT, data write in the body in json format)
Telegram Registration
 {
 "registerType":"service",
 "Id":"serviceId",
 "type":"crowControl",
 "topic":"/overtemperature/...",
 "attribute":{"botId": "Smartmubot"
              "chatID": "chatID1"
               "message":"switchon","switchoff","start"
             }
 }
 Return (in body):
 {"registerStatus":"Success","errorType":"None"}
