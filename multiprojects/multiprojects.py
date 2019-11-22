import threading
import tkinter as tk

import requests
import cv2

from camera_basler import CameraBasler
from pekat_instance import PekatInstance
from config import config

pekat_instance = None
app_run = False


def camera_status_updated(status):
    print("Update camera status ", status)
    l2.config(text=status.get("label"))


def send_image(img):
    try:
        _, i = cv2.imencode('.jpg', img)
        # send to pekat
        return requests.get(
            url='http://127.0.0.1:'+str(config.get('port'))+'/analyze_image',
            files={'file': bytearray(i)},
        )
    except Exception as e:
        print("ERROR send image to pekat", e)

    return None


def camera_sender():
    while True:
        frame = next(camera_generator)
        if app_run:
            send_image(frame)


def set_msg(text):
    l1.config(text=text)


def start_project(line):
    global pekat_instance, app_run
    path = None

    # stop running instance
    if pekat_instance:
        app_run = False
        pekat_instance.kill()

    # find current project
    for i in config['projects_map']:
        if line.startswith(i["key"]):
            path = i['path']

    # project not found
    if not path:
        set_msg("unknown key")
        return

    # update message
    t = threading.Thread(target=set_msg, args=("Starting project ... ",))
    threading.Event()
    t.start()

    # start pekat
    pekat_instance = PekatInstance(port=config.get('port'), path=path)
    app_run = True

    # update message
    t = threading.Thread(target=set_msg, args=("Project is running ",))
    threading.Event()
    t.start()


def callback_press_enter(event):
    line = e1.get()
    # delete text in input
    e1.delete(0, 'end')
    t = threading.Thread(target=start_project, args=(line,))
    threading.Event()
    t.start()


if __name__ == '__main__':
    info = ""
    for i in config['projects_map']:
        info += i["path"] + " - " + i["key"] + "\n"

    master = tk.Tk()
    master.title("PEKAT")
    l1 = tk.Label(master, text="None project", )
    l1.grid(row=0)

    l2 = tk.Label(master, text="camera")
    l2.grid(row=1)

    e1 = tk.Entry(master)
    e1.grid(row=2)

    # show list of projects
    l3 = tk.Label(master, text=info)
    l3.grid(row=3)

    # set callback on press enter
    e1.bind("<Return>", callback_press_enter)

    # init camera
    camera = CameraBasler(config.get("camera_settings"))
    camera.status_updated_callback(camera_status_updated)
    camera_generator = camera.get_image()

    # run camera - send image to clients
    camera_thread = threading.Thread(target=camera_sender, args=())
    camera_thread.start()

    master.mainloop()
