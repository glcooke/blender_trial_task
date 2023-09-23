import datetime
import platform


class Scenario:
    def __init__(self, name, func, blend_file, output_image, output_log):
        self._name = name
        self._func = func
        self._blend_file = blend_file
        self._output_image = output_image
        self._output_log = output_log
        self._start = None
        self._end = None
        self._duration = None
        self._system = platform.uname()._asdict()

    def get_func(self):
        return self._func

    def get_name(self):
        return self._name

    def get_output(self):
        return self._output_log

    def start_test(self):
        self._start = datetime.datetime.now()

    def end_test(self):
        self._end = datetime.datetime.now()
        self._duration = self._end - self._start

    def get_json(self):
        info = {
            "Test name": self._name,
            "Date and time started": str(self._start),
            "Date and time ended": str(self._end),
            "Test duration": str(self._duration),
            "System information": self._system,
        }

        return info
