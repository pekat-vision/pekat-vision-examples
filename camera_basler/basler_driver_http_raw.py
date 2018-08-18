
# Requirements:
#
#  - Install Pylon from https://www.baslerweb.com/en/sales-support/downloads/software-downloads/#os=linuxx86;version=all;type=pylonsoftware;language=all
#  - Install PyPylon from https://github.com/basler/pypylon

from pypylon import pylon
import requests

# Init camera - load settings from file. You can get such file from Pylon Viewer in menu Camera -> Save features...
camera_settings_file = "camera_settings.pfs"  # name of the file

camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
camera.Open()
pylon.FeaturePersistence_Load(camera_settings_file, camera.GetNodeMap(), True)


camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        frame = grabResult.Array
        shape = frame.shape

        # Important! Set Pixel Format in the camera to BGR 8 (for a color image) otherwise you would need to convert the image here.
        
        # Call PEKAT VISION (assuming PEKAT VISION runs on 127.0.0.1:8100)
        response = requests.post(
            url='http://127.0.0.1:8100/analyze_raw_image?width='+str(shape[1])+'&height='+str(shape[0]),
            data=frame.tobytes(),
            headers={'Content-Type': 'application/octet-stream'}
        )

        print(response.json())

    grabResult.Release()
