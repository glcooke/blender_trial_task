import datetime
import platform
import psutil


# Define a class for representing test scenarios
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
            'RAM': str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB"
        }

    # Getter method for retrieving the test function associated with the scenario
    def get_func(self):
        return self._func

    # Getter method for retrieving the name of the test scenario
    def get_name(self):
        return self._name

    # Method to record the start time of the test
    def start_test(self):
        self._start = datetime.datetime.now()

    # Method to record the end time of the test and calculate its duration
    def end_test(self):
        self._end = datetime.datetime.now()
        self._duration = self._end - self._start

    # Getter method for retrieving the start time of the test
    def get_start(self):
        return self._start

    # Setter method for setting the status of the test (e.g., "OK" or "FAIL")
    def set_status(self, status):
        self._status = status

    # Getter method for retrieving the end time of the test
    def get_end(self):
        return self._end

    # Getter method for retrieving the duration of the test
    def get_duration(self):
        return self._duration

    # Method to return JSON dump
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
