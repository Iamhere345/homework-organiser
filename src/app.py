import sys
from datetime import datetime

from PySide6 import QtWidgets

from task_list import *
from task import *
from task_edit import *
from utils import *

# main application class
class HomeworkOrganiser(QtWidgets.QWidget):
    def __init__(self, tasks: list[Task]):
        super().__init__()

        self.setWindowTitle("Homework Organiser")

        self.main_layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.main_layout)

        self.tasks = tasks

        # create task view and add it to the app
        self.task_view = TaskView(self.tasks, self.set_selected_task)
        self.task_view_container = QtWidgets.QWidget()
        self.task_view_container.setLayout(self.task_view)
        self.main_layout.addWidget(self.task_view_container, stretch=1)
        self.task_view_container.adjustSize()

        # add seperator line between the task list and edit form
        self.seperator_line = SeperatorLine(True)
        self.main_layout.addWidget(self.seperator_line, stretch=1)

        # create the edit view and add it to the app
        self.edit_view = TaskEdit()
        self.edit_view_container = QtWidgets.QWidget()
        self.edit_view_container.setLayout(self.edit_view)
        self.edit_view.updated.connect(self.task_updated)
        self.edit_view.created.connect(self.task_created)
        self.edit_view.deleted.connect(self.task_deleted)
        self.main_layout.addWidget(self.edit_view_container, stretch=2)

    # callback for when a task is selected in the task list
    def set_selected_task(self, index):
        self.edit_view.set_selected_task(self.tasks[index], index)
    
    # callback for when a task is updated in the task edit form
    def task_updated(self):
        self.task_view.redraw_list()
    
    # callback for when a task is created in the task edit form
    def task_created(self, task: Task):
        print("task created")
        self.tasks.append(task)
        self.task_view.redraw_list()
    
    # callback for when a task is deleted in the edit form
    def task_deleted(self, index: int):
        print("task deleted")
        del self.tasks[index]
        self.task_view.redraw_list()
    
    # callback for when new tasks are loaded from a file
    def on_tasks_loaded(self, tasks: list[Task]):
        self.tasks = tasks

        self.task_view.tasks = tasks
        self.task_view.redraw_list()

        self.edit_view.clear_selected_task()

