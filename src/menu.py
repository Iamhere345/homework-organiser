from PySide6 import QtWidgets
from PySide6 import QtGui

from task import *
from file_io import *

class AppMenuBar(QtWidgets.QMenuBar):
    def __init__(self):
        super().__init__(parent=None)

        self.tasks = []
        #self.setNativeMenuBar(False)

        file_menu = self.addMenu("File")

        self.save = QtGui.QAction("Save")
        self.save.triggered.connect(self.on_save)
        file_menu.addAction(self.save)

        self.addSeparator()

        self.open = QtGui.QAction("Open")
        self.open.triggered.connect(self.on_open)
        file_menu.addAction(self.open)
    
    def on_save(self):
        path, _ = QtWidgets.QFileDialog.getSaveFileName()

        if not path is None:
            save_tasks(path, self.tasks)

    def on_open(self):
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("Task files (*.tsk)")

        if file_dialog.exec():
            path = file_dialog.selectedFiles()
            loaded_tasks = load_tasks(path[0])
            
            if not loaded_tasks is None:
                self.tasks = loaded_tasks
        