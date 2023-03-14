from Entity.Task import *
from Entity.Progress import *

class DataBase():
    def __init__(self):
        self.progresses = []
        self.tasks = []

class TaskFactory():
    def __init__(self):
        self.maxIndex = 0
    
    def MaxIndexCalculation(self):
        self.maxIndex = self.maxIndex + 1

    def New(self, taskDescription : str, creationTime : str, status : str) -> Task:
        task = Task()
        task.description = taskDescription
        task.creationTime = creationTime
        task.status = status
        task.id = self.maxIndex

        self.MaxIndexCalculation()
        return task
    
    def Delete(self, index : int, tasks : list) -> list:
        tasks.pop(index)
        return tasks


class ProgressFactory():
    def New(self, taskId : int, progressDescription : str) -> Progress:
        progress = Progress()
        progress.taskId = taskId
        progress.description = progressDescription
        return progress
    
    def Delete(self, index : int, progresses : list) -> list:
        progresses.pop(index)
        return progresses

    def Modify(self, progress : Progress, progressDescription : str) -> Progress:
        progress.description = progressDescription
    