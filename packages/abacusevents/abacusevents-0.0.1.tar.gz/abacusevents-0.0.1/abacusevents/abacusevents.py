import json
from abc import ABC
from .utils import lowercase_first
from datetime import datetime


class Event(ABC):
    def __init__(self, session_id=None, task_id=None, job_id=None, data=None, done=False):
        self.sessionId = session_id
        self.taskId = task_id
        self.jobId = job_id
        self.data = data
        self.done = done
        self.observedAt = str(datetime.now())

    def serialize(self):
        a_dict = self.__dict__
        a_dict['event'] = lowercase_first(self.__class__.__name__)
        return json.dumps(a_dict).encode('utf-8')


class Ping(Event):
    pass


class Pong(Event):
    pass
