import sys
sys.path.insert(1, 'F:\Projetos\Eng Software\ToDo_v2')

from DataBase import *

class TaskService():
    
    def __init__(self, taskDataBase : DataBase, taskFactory : TaskFactory):
        self.taskDataBase = taskDataBase
        self.taskFactory = taskFactory

    def AddTask(self, taskDescription : str, taskDate : str, tasksStatus : str) -> bool:
        task = self.taskFactory.New(taskDescription, taskDate, tasksStatus)
        self.taskDataBase.tasks.append(task)
        return True

    def RemoveTask(self, id : int) -> bool:

        thereIsTask = False
        tasksSize = len(self.taskDataBase.tasks)

        for index in range(tasksSize):
            if self.taskDataBase.tasks[index].id == id:
                thereIsTask = True
                self.taskDataBase.tasks = self.taskFactory.Delete(index, self.taskDataBase.tasks)
                break
                            
        return thereIsTask
    
    def ModifyTask(self, taskId : int, taskDescription : str,
                   taskDate : str, taskStatus : status) -> Task:

        tasksAmount = len(self.taskDataBase.tasks)
        taskModified = False
        
        for index in range(tasksAmount):            
            task = self.taskDataBase.tasks[index]

            if task.id == taskId:
                self.taskFactory.Modify(task, taskDescription, taskDate, taskStatus)
                taskModified = True
                break
        
        return taskModified