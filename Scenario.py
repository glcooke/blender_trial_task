import datetime
import platform
import psutil


class Scenario:
    def __init__(self, name, func):
        self._name = name
        self._func = func
        self._status = None
        self._start = None
        self._end = None
        self._duration = None
        self._system = {
            'platform': platform.system(),
            'CPU': platform.processor(),
            'RAM': str(round(psutil.virtual_memory().total / (1024.0 ** 3)))+" GB"
        }


    def get_func(self):
        return self._func

    def get_name(self):
        return self._name

    def start_test(self):
        self._start = datetime.datetime.now()

    def end_test(self):
        self._end = datetime.datetime.now()
        self._duration = self._end - self._start

    def get_start(self):
        return self._start

    def set_status(self, status):
        self._status = status

    def get_end(self):
        return self._end

    def get_duration(self):
        return self._duration

    def get_json(self):
        info = {
            "Test name": self._name,
            "Test status": self._status,
            "Date and time started": str(self._start),
            "Date and time ended": str(self._end),
            "Test duration": str(self._duration),
            "System information": self._system,
        }

        return info
