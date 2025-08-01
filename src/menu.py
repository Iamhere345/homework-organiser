from PySide6 import QtWidgets
from PySide6 import QtGui

from task import *
from file_io import *

# wrapper class for the application menu bar
# create 'save' and 'open' buttons which pass file paths to file_io
class AppMenuBar(QtWidgets.QMenuBar):
    def __init__(self):
        super().__init__()

        # this class is the owner of the task list
        # ! the task list is an important data structure:
        # ! it stores the information for each task that the user has entered
        self.tasks = []

        file_menu = self.addMenu("File")

        # add 'save' button to file menu
        self.save = QtGui.QAction("Save")
        self.save.triggered.connect(self.on_save)
        file_menu.addAction(self.save)

        self.addSeparator()

        # add 'open' button to file menu
        self.open = QtGui.QAction("Open")
        self.open.triggered.connect(self.on_open)
        file_menu.addAction(self.open)
    
    # callback for save button
    # will save the tasks to a file when the user selected a save location
    def on_save(self):
        # prompt user for save location
        path, _ = QtWidgets.QFileDialog.getSaveFileName()

        if not path is None:
            save_tasks(path, self.tasks)

    # callback for open button
    # will load tasks from a user selected file
    def on_open(self):
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("Task files (*.tsk)")

        if file_dialog.exec():
            # prompt user to select file, pass file path to load_tasks()
            path = file_dialog.selectedFiles()
            loaded_tasks = load_tasks(path[0])
            
            # refuse to load tasks if load_tasks failed
            if not loaded_tasks is None:
                self.tasks = loaded_tasks
        