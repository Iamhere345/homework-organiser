import sys
from datetime import datetime

from PySide6 import QtWidgets

from task_list import *
from task import *
from task_edit import *
from utils import *

class HomeworkOrganiser(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Homework Organiser")

        self.main_layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.main_layout)

        # hardcoded testing values
        self.tasks = [
            Task("a", datetime(2025, 7, 1), "e", TaskPriority.MEDIUM),
            Task("b", datetime(2018, 10, 10), "d", TaskPriority.LOW),
            Task("c", datetime(2022, 8, 12), "c", TaskPriority.HIGH),
            Task("d", datetime(2026, 12, 4), "b", TaskPriority.VERY_HIGH),
            Task("e", datetime(2011, 3, 22), "a", TaskPriority.LOW),
        ]

        self.task_view = TaskView(self.tasks)
        self.task_view_container = QtWidgets.QWidget()
        self.task_view_container.setLayout(self.task_view)
        self.main_layout.addWidget(self.task_view_container, stretch=1)
        self.task_view_container.adjustSize()

        self.seperator_line = SeperatorLine(True)
        self.main_layout.addWidget(self.seperator_line, stretch=1)

        self.edit_view = TaskEdit()
        self.edit_view_container = QtWidgets.QWidget()
        self.edit_view_container.setLayout(self.edit_view)
        self.main_layout.addWidget(self.edit_view_container, stretch=2)
