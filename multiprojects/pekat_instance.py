import os
import signal
import sys
import threading
import subprocess

from config import config


class PekatInstance:

    def __init__(self, port, path, camera=None, start_cb=None):
        self.lock = threading.Lock()
        self.port = str(port)
        self.start_cb = start_cb
        self.path = path
        self.camera = camera

        t = threading.Thread(target=self.__start_instance, args=())
        threading.Event()
        t.start()
        self.lock.acquire()
        self.lock.acquire()

    def __start_instance(self):
        bin_path = os.path.join(config['pekat_path'], "resources/bin")
        server_path = os.path.join(config['pekat_path'], "server/server.exe")
        my_env = os.environ.copy()

        my_env["PATH"] = bin_path + ";" + my_env["PATH"]
        my_env["Path"] = bin_path
        my_env["LD_LIBRARY_PATH"] = bin_path

        params = [server_path, "-d", self.path, "-port", self.port]

        self.process = subprocess.Popen(
            params,
            env=my_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        while True:
            next_line = self.process.stdout.readline().decode()
            print(next_line)
            if next_line == '' and self.process.poll() is not None:
                break
            sys.stdout.flush()
            if next_line.find("__SERVER_RUNNING__") != -1:
                print(self.path)
                self.lock.release()
                if self.start_cb:
                    self.start_cb()

            else:
                print(next_line)

    def kill(self):
        self.process.terminate()
