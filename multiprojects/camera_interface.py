import abc

RUNNING_STATUS = {'run': True, 'label': 'Camera running'}
STOP_STATUS = {'run': False, 'label': 'Camera - sopped'}
STARTING_STATUS = {'run': False, 'label': 'Camera starting'}


class CameraInterface(abc.ABC):
    status = STOP_STATUS
    callback = None

    @abc.abstractmethod
    def get_image(self):
        pass

    def status_updated_callback(self, func):
        self.callback = func

    def set_status(self, next_status):
        if self.callback:
            self.callback(next_status)
        self.status = next_status