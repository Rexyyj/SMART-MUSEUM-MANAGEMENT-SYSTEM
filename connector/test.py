# -*- coding: utf-8 -*-
# @Time    : 4/10/2021 2:57 PM
# @Author  : Rex Yu
# @Mail    : jiafish@outlook.com
# @Github  : https://github.com/Rexyyj

from random import seed
from random import randint
import cv2

seed(1)
rawAddr = "./configs/raw-headshot/"
rawNum = randint(1, 2)
rawImg = cv2.imread(rawAddr +  "1.png")
rawImg = cv2.resize(rawImg, (480, 640), interpolation=cv2.INTER_AREA)
generatedImg = cv2.rectangle(rawImg, (80, 450), (400, 50), (0, 255, 0), 2)
generatedImg = cv2.putText(generatedImg, "38.5", (210, 40), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 0, 255), 2, cv2.LINE_AA)
cv2.imshow("myimage",generatedImg)
cv2.waitKey(0)
cv2.destroyAllWindows()
