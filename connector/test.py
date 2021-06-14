from ImageManager import ImageManager
import requests
import cv2

manager = ImageManager("./")
response = requests.get("http://172.17.0.1:8091/1",None)
img = manager.exactImageFromResponse(response)
cv2.imwrite("./test.jpg",img)