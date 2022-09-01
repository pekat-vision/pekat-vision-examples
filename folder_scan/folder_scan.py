import logging
import os
from time import sleep

from watchdog.events import FileSystemEventHandler, FileCreatedEvent
from watchdog.observers import Observer

from PekatVisionSDK import Instance

logging.getLogger().setLevel(logging.INFO)


SUPPORTED_EXTENSIONS = [".png", ".jpg", ".jpeg", ".bmp"]
PATH_TO_IMAGES_FOLDER = "C:\\Users\\pekat\\Pictures"


class MyHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.p = Instance(host="127.0.0.1", port=8000, already_running=True)

    def on_created(self, event: FileCreatedEvent):
        logging.info(event.src_path)
        logging.info(os.path.splitext(event.src_path))
        if os.path.splitext(event.src_path)[1].lower() in SUPPORTED_EXTENSIONS:
            init_size = -1
            current_size = 0
            while init_size != current_size:
                init_size = current_size
                sleep(0.001)
                current_size = os.path.getsize(event.src_path)
            logging.info("Sending to PEKAT VISION.")
            try:
                context = self.p.analyze(event.src_path)
                logging.info("Image analyzed:" + str(context))
            except Exception as e:
                if hasattr(e, 'message'):
                    logging.error(e.message)
                else:
                    logging.error(e)
        else:
            logging.warning("Invalid image format, ignoring...")


def main():
    event_handler = MyHandler()

    observer = Observer()
    observer.schedule(event_handler, PATH_TO_IMAGES_FOLDER)

    observer.start()

    try:
        while True:
            logging.info("Sleeping for 1 second...")
            sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info("Exiting, bye!")


if __name__ == "__main__":
    main()
