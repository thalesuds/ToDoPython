import PySimpleGUI as sg
from Service.ProgressService import *
from Service.TaskService import *

dataBase = DataBase()

taskFactory = TaskFactory()
taskService = TaskService(dataBase, taskFactory)

progressFactory = ProgressFactory()
progressService = ProgressService(progressFactory, dataBase)

class TasksSimpleGUI:
    def __init__(self):
        self.simpleGui = sg
        self.tasks = []
        self.date = []
        self.status = []
        self.rowCounter = 0

    def FirstRow(self) -> list:
        row = [self.simpleGui.Column([[self.simpleGui.Text('', size=(3, 1)),
               self.simpleGui.Text('Tarefas', background_color='White', text_color='Black', size=(15, 1)),
               self.simpleGui.Text('Data', background_color='White', text_color='Black', size=(15, 1)),
               self.simpleGui.Text('Status', background_color='White', text_color='Black', size=(15, 1))]], key = 'firstRow')
               ]

        return row

    def CreateLayout(self) -> list:

        inputDescriptionLine = [
            self.simpleGui.Column([[
             self.simpleGui.Text('Tarefa'),
             self.simpleGui.Text('                                                                   '),
             self.simpleGui.Text('Data'), 
             self.simpleGui.Text('        '), 
             self.simpleGui.Text('Status')]], key = 'inputDescription')
        ]

        taskInputsLine = [
            self.simpleGui.Column([[
            self.simpleGui.Input(''), self.simpleGui.Input('', size=(10, 20)), self.simpleGui.Input('', size=(10, 30)),
            self.simpleGui.Button('Salvar')]], key = 'inputLine')
        ]

        buttonsLine = [
            self.simpleGui.Column([[
            self.simpleGui.Button('Deletar'),
            self.simpleGui.Button('Progresso')]], key = 'firsRow')
        ]

        layout = [[inputDescriptionLine],
                  [taskInputsLine],
                  [self.FirstRow()],
                  [buttonsLine]
        ]

        return list(layout)

    def CreateWindow(self, layout: list) -> sg.Window:
        return self.simpleGui.Window('ToDo List', layout=layout)

    def AddRow(self, task : str, date : str, status : str) -> list:

        row = [
        self.simpleGui.Checkbox('', key = 'Checkbox'+str(self.rowCounter)),
        self.simpleGui.Text(task, background_color='White', text_color='Black', size=(15, 1), key='Task'+str(self.rowCounter)),
        self.simpleGui.Text(date, background_color='White', text_color='Black', size=(15, 1), key = 'Date'+ str(self.rowCounter)),
        self.simpleGui.Text(status, background_color='White', text_color='Black', size=(15, 1), key = 'Status'+str(self.rowCounter))
    ]
        self.rowCounter += 1
        return list(row)

    def ExtendWindow(self, window: sg.Window, task: str, date: str, status: str):
        window.extend_layout(window['firstRow'],
                             [self.AddRow(task, date, status)])

    def DeleteRow(self):
        self.rowCounter = 0

    def RefreshWindow(self, window : sg.Window) -> sg.Window:
        window.close()
        layout = self.CreateLayout()
        window = self.CreateWindow(layout)
        
        return window

class ProgressSimpleGui:
    def __init__(self):
        self.simpleGui = sg
        self.rowCounter = 0
    
    def CreateLayout(self):

        descriptionAndInputRow = [self.simpleGui.Column([[
               self.simpleGui.Text('Descreva o Progresso', background_color='White', text_color='Black', size=(20, 1), justification='center'),
               self.simpleGui.Input('', size=(30, 1))]], key = 'progressDescription')
              ]

        saveButton = [
            self.simpleGui.Column([[self.simpleGui.Button('Salvar')]], key = 'saveButton')
                ]

        tableFirstRow = [self.simpleGui.Column([[
               self.simpleGui.Text('Descrição do Progresso ', background_color='White', 
                                   text_color='Black', size=(30, 1), justification='center')]], key = 'tableFirstRow')
               ]

        deleteButton = [self.simpleGui.Column([[
                self.simpleGui.Button('Deletar')]], key = 'deleteButton')
                ]

        layout = [
            [descriptionAndInputRow, saveButton],
            [tableFirstRow],
            [deleteButton]
        ]

        return layout

    def WindowCreate(self, layout : list) -> sg.Window:
        window = self.simpleGui.Window('Registro de Progresso', layout, element_justification= 'c', finalize= True)
        return window

    def AddRow(self, progress : str):

        row = [
        self.simpleGui.Checkbox('', key = 'Checkbox'+str(self.rowCounter)),
        self.simpleGui.Text(progress, background_color='White', text_color='Black', size=(20, 1), key='Progress'+str(self.rowCounter)),
    ]
        self.rowCounter += 1
        return list(row)
    
    def ExtendWindow(self, window : sg.Window, progress : str):
        window.extend_layout(window['tableFirstRow'],[self.AddRow(progress)])
    
    def DeleteRow(self, index : int):
        self.rowCounter = 0

    def AddExistentsProgress(self, window : sg.Window, progresses : list):
        for i in range(len(progresses)):
            progress = progresses[i].description
            self.ExtendWindow(window, progress)
    
    def RefreshWindow(self, window : sg.Window, progresses : list) -> sg.Window:
        window.close()
        layout = self.CreateLayout()
        window = self.WindowCreate(layout)

        self.AddExistentsProgress(window, progresses)    
        return window

class ProgressGuiHandler:
    def __init__(self, gui : ProgressSimpleGui):
        self.gui = gui
        self.values = []
        self.event = ''
        self.layout = self.gui.CreateLayout()
        self.window = ''
        self.index = []
        self.layoutInUse = False
    
    def OpenWindow(self):
        self.window = self.gui.WindowCreate(self.layout)
        self.layoutInUse = True

    def GetIndexOfSelectedCheckbox(self):
        valuesAmount = len(self.values)

        if valuesAmount > 1:
            for i in range(valuesAmount-1):
                keyName = 'Checkbox'+str(i)

                if keyName in self.values.keys():                    
                    if self.values[keyName] == True:
                        self.index.append(i)

        else:
            return False

        return True

    def WindowHandler(self, taskId : int):

        if self.layoutInUse == False:
            self.OpenWindow()
        
        else:
            progresses = progressService.ReturnProgresses(taskId)
            self.window = self.gui.RefreshWindow(self.window, progresses)

        while True:
            self.event, self.values = self.window.read()

            if self.event == sg.WIN_CLOSED:
                break

            elif self.event == 'Salvar':
                progressService.AddProgress(taskId, self.values[0], dataBase.progresses)
                self.gui.ExtendWindow(self.window, self.values[0])
            
            elif self.event == 'Deletar':

                thereIsProgresses = self.GetIndexOfSelectedCheckbox()

                if thereIsProgresses == True:
                    for i in range(len(self.index)):
                            index = self.index[i]
                            self.gui.DeleteRow(index)
                            progressService.DeleteSpecificProgress(taskId, index)

                    progresses = progressService.ReturnProgresses(taskId)
                    self.window = self.gui.RefreshWindow(self.window, progresses)
                    self.index = []
                
                else:
                    self.gui.simpleGui.popup_ok('Não há progressos para serem deletadas', title = 'Aviso')
            
class TaskGuiHandler:
    def __init__(self, gui : TasksSimpleGUI):
        self.event = ''
        self.values = []
        self.gui = gui
        self.layout = self.gui.CreateLayout()
        self.taskWindow = self.gui.CreateWindow(self.layout)
        self.index = []
        self.lineId = []    

        self.progressWindowsManagement = []

    def GetIndexOfSelectedCheckbox(self) -> bool:

        valuesAmount = len(self.values)
        if valuesAmount > 3:
            for i in range(valuesAmount-3):
                keyName = 'Checkbox'+str(i)
                if keyName in self.values.keys():
                    
                    if self.values[keyName] == True:
                        self.index.append(i)
        else:
            return False

        return True

    def PresentTasksRows(self):
        tasksAmount = len(dataBase.tasks)
        for i in range(tasksAmount):
            task = dataBase.tasks[i].description
            date = dataBase.tasks[i].creationTime
            status = dataBase.tasks[i].status
            
            self.gui.ExtendWindow(self.taskWindow, task, date, status)


    def WindowHandler(self):

        while True:
            self.event, self.values = self.taskWindow.read()

            if self.event == sg.WIN_CLOSED:
                break

            elif self.event == 'Salvar':
                taskDescription = self.values[0]
                date = self.values[1]
                status = self.values[2]

                taskService.AddTask(taskDescription, date, status)    

                self.gui.ExtendWindow(self.taskWindow, taskDescription, date, status)
                progressGui = ProgressSimpleGui()
                progressHandler = ProgressGuiHandler(progressGui) 
                self.progressWindowsManagement.append(progressHandler)
            
            elif self.event == 'Deletar':
                thereIsTasks = self.GetIndexOfSelectedCheckbox()

                if thereIsTasks == True:
                    for i in range(len(self.index)):
                        index = self.index[i]
                        self.gui.DeleteRow()
                        self.progressWindowsManagement.pop(index)
                        taskService.RemoveTask(index)
                        progressService.DeleteProgressesFromTask(index)

                    self.taskWindow = self.gui.RefreshWindow(self.taskWindow)
                    self.PresentTasksRows()
                    self.index = []

                else:
                    self.gui.simpleGui.popup_ok('Não há tarefas para serem deletadas', title = 'Aviso')
            
            elif self.event == 'Progresso':
                thereIsTasks = self.GetIndexOfSelectedCheckbox()

                if thereIsTasks == True:
                    for i in range(len(self.index)):
                        index = self.index[i]
                        self.progressWindowsManagement[index].WindowHandler(index)
                    self.index = []

taskGui = TasksSimpleGUI()
taskHandler = TaskGuiHandler(taskGui)
taskHandler.WindowHandler()
