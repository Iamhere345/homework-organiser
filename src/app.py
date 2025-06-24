import sys
from datetime import datetime

from PySide6 import QtWidgets

from task_list import TaskList
from task import *

class HomeworkOrganiser(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Homework Organiser")

        self.main_layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.main_layout)

        self.tasks = []

        for i in range(20):
            self.tasks.append(Task(f"Task {i}", datetime.now(), "Applied Computing", TaskPriority.LOW))

        self.task_list = TaskList(self.tasks)
        self.setCentralWidget(self.task_list)
