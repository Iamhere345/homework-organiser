from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLineEdit,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QListWidgetItem,
    QListView
)

from datetime import datetime

from task import *

class TaskCard(QListWidgetItem):
    def __init__(self, task: Task):
        self.task = task
        super().__init__(f"{task.get_title()}\n{str(task.get_due_date())}\n{task.get_class()}")

class TaskList(QListView):
    def __init__(self):
        super().__init__()