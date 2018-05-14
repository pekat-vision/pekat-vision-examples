import cv2
import requests
import numpy as np

# camera 0
cap0 = cv2.VideoCapture(0)
# camera 1
cap1 = cv2.VideoCapture(1)

while True:
    _, frame0 = cap0.read()
    _, frame1 = cap1.read()
    shape = frame0.shape

    # create empty image
    f = np.empty((shape[0], shape[1] * 2, shape[2]), dtype="uint8")

    # add first image
    f[:, :shape[1]] = frame0
    # add second image
    f[:, shape[1]:] = frame1

    response = requests.post(
        url='http://127.0.0.1:8000/analyze_raw_image',
        data={'width': f.shape[1], 'height': f.shape[0]},
        files={'array': f.tobytes()}
    )

    print(response.json())

