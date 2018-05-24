import time

import cv2
import requests

cap = cv2.VideoCapture(0)

# you can set frame size
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)

port = 8000

url = 'http://127.0.0.1:'+str(port)+'/analyze_image'
img = cv2.imread('cat.jpg')
_, data = cv2.imencode('.jpg', img)
r = requests.post(url=url, data=data.tobytes(), headers={'Content-Type': 'application/octet-stream'})
print(r.json())
