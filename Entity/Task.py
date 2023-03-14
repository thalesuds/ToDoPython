from enum import Enum

class status(Enum):
    pending = 0
    completed = 1

class Task():
    def __init__(self):
        self.description = ''
        self.creationTime = ''
        self.status = ''
        self.id = None