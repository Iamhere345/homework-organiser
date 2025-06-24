from PySide6 import QtWidgets

from datetime import datetime

from task import *

class TaskCard(QtWidgets.QGroupBox):
    def __init__(self, task: Task):
        super().__init__()

        hbox = QtWidgets.QHBoxLayout()
        vbox = QtWidgets.QVBoxLayout()

        title = QtWidgets.QLabel(f"{task.get_title()}")
        due_date = QtWidgets.QLabel(f"{task.get_due_date().strftime("%d/%m/%y")}")
        class_name = QtWidgets.QLabel(f"{task.get_class()}")

        vbox.addWidget(title)
        vbox.addWidget(due_date)
        vbox.addWidget(class_name)

        hbox.addLayout(vbox)

        checkbox = QtWidgets.QCheckBox("Mark as complete")
        hbox.addWidget(checkbox)

        super().setLayout(hbox)

class TaskList(QtWidgets.QScrollArea):
    def __init__(self, tasks: list[Task]):
        super().__init__()

        self.holder_widget = QtWidgets.QWidget()
        self.vbox = QtWidgets.QVBoxLayout()

        self.task_cards = []

        for task in tasks:
            task_card = TaskCard(task)
            self.vbox.addWidget(task_card)

            self.task_cards.append(task_card)
        
        self.holder_widget.setLayout(self.vbox)
        super().setWidget(self.holder_widget)

