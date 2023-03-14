import sys
sys.path.insert(1, 'F:\Projetos\Eng Software\ToDo_v2')

from DataBase import *

class ProgressService():
    def __init__(self, progressFactory : ProgressFactory, dataBase : DataBase):
        self.progressFactory = progressFactory
        self.dataBase = dataBase

    def AddProgress(self, taskId : int, progressDescription : str, dataBase : DataBase) -> bool:
        progress = self.progressFactory.New(taskId, progressDescription)
        self.dataBase.progresses.append(progress)
        return True

    def ReturnProgresses(self, taskId : int) -> list:

        progressesAmount = len(self.dataBase.progresses)
        selectedProgresses = []

        for index in range(progressesAmount):
            progress = self.dataBase.progresses[index]

            if progress.taskId == taskId:
                selectedProgresses.append(progress)
        
        return selectedProgresses
    
    def DeleteSpecificProgress(self, taskId : int, progressIndex : int) -> bool:
        
        selectedProgresses = self.ReturnProgresses(taskId)
        progressAmount = len(selectedProgresses)
        deleted = False

        for i in range(len(self.dataBase.progresses)):
            progressDescription = self.dataBase.progresses[i].description
            progresstaskId = self.dataBase.progresses[i].taskId

            if progresstaskId == taskId and selectedProgresses[progressIndex].description == progressDescription:
                self.dataBase.progresses = self.progressFactory.Delete(i, self.dataBase.progresses)
                deleted = True
                break


        return deleted

    def DeleteProgressesFromTask(self, taskId : int):

        for i in range(len(self.dataBase.progresses)):
            progressIdTracker = self.dataBase.progresses[i].taskId

            if progressIdTracker == taskId:
                self.dataBase.progresses.pop(i)
