from PySide6 import QtWidgets
from PySide6 import QtGui
from PySide6 import QtCore

from task import *
from file_io import *

# wrapper class for the application menu bar
# create 'save' and 'open' buttons which pass file paths to file_io
class AppMenuBar(QtWidgets.QMenuBar):
    tasks_loaded = QtCore.Signal(list[Task])

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
        self.save.setShortcut(QtGui.QKeySequence.StandardKey.Save)
        file_menu.addAction(self.save)

        self.addSeparator()

        # add 'open' button to file menu
        self.open = QtGui.QAction("Open")
        self.open.triggered.connect(self.on_open)
        self.open.setShortcut(QtGui.QKeySequence.StandardKey.Open)
        file_menu.addAction(self.open)

        # add 'close' button to file menu
        self.close_file = QtGui.QAction("Close")
        self.close_file.triggered.connect(self.on_close)
        self.close_file.setShortcut(QtGui.QKeySequence.StandardKey.Close)
        file_menu.addAction(self.close_file)
    
    # callback for save button
    # will save the tasks to a file when the user selected a save location
    def on_save(self):
        # prompt user for save location
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setWindowTitle("Save tasks to file")
        file_dialog.setDefaultSuffix(".tsk")
        path, _ = QtWidgets.QFileDialog.getSaveFileName()

        if not path is None:
            # append the task file extension to the path
            save_tasks(path + ".tsk", self.tasks)

    # callback for open button
    # will load tasks from a user selected file
    def on_open(self):
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setWindowTitle("Load tasks from file")
        file_dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilters(["Task Files (*.tsk)", "All Files (*)"])

        if file_dialog.exec():
            # prompt user to select file, pass file path to load_tasks()
            path = file_dialog.selectedFiles()
            loaded_tasks = load_tasks(path[0])
            
            # refuse to load tasks if load_tasks failed
            if not loaded_tasks is None:
                self.tasks = loaded_tasks
                self.tasks_loaded.emit()
    
    # callback for close button
    # will clear the task list
    def on_close(self):
        self.tasks = []
        self.tasks_loaded.emit()