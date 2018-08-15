import cv2
import requests

cap = cv2.VideoCapture(0)

# you can set frame size
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)

while True:
    # get frame from camera
    ret, frame = cap.read()
    _, data = cv2.imencode('.jpg', frame)
    # send frame to PEKAT VISION
    response = requests.post(
        url='http://127.0.0.1:8000/analyze_image',
        data=data.tobytes(),
        headers={'Content-Type': 'application/octet-stream'}
    )

    print(response.json())

