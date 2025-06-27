from PySide6 import QtWidgets
from PySide6 import QtCore
import PySide6

from datetime import datetime

from task import *

class SortType(Enum):
    NAME = 0
    CLASS = 1
    DUEDATE = 2
    PRIORITY = 3

    def __str__(self):
        match self:
            case SortType.NAME:
                return "Name"
            case SortType.CLASS:
                return "Class"
            case SortType.DUEDATE:
                return "Due Date"
            case SortType.PRIORITY:
                return "Priority"
            case _:
                return f"Unknown ({self.value})"

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

        self.main_vbox = QtWidgets.QVBoxLayout()
        
        self.holder_widget = QtWidgets.QWidget()
        self.list_vbox = QtWidgets.QVBoxLayout()

        self.task_cards: list[TaskCard] = []

        for task in tasks:
            task_card = TaskCard(task)
            self.list_vbox.addWidget(task_card)

            self.task_cards.append(task_card)
        
        self.holder_widget.setLayout(self.list_vbox)
        super().setWidget(self.holder_widget)
    
    def clear_list(self):
        for card in self.task_cards:
            card.deleteLater()

        self.task_cards.clear()
    
    # assumes task_cards is empty, otherwise duplicates will be created
    def populate_list(self, tasks: list[Task]):
        for task in tasks:
            task_card = TaskCard(task)
            self.list_vbox.addWidget(task_card)

            self.task_cards.append(task_card)

# this class combines the TaskList with a header and manages the sorting of tasks
class TaskView(QtWidgets.QVBoxLayout):
    def __init__(self, tasks: list[Task]):
        super().__init__()

        self.tasks = tasks
        self.sort_type = SortType.NAME

        self.show_header()
        self.show_list()

    def show_header(self):
        self.header_hbox = QtWidgets.QHBoxLayout()

        self.title = QtWidgets.QLabel('<h2>Tasks</h2>')
        self.header_hbox.addWidget(self.title)

        self.sort_btn = QtWidgets.QPushButton(f"Sort by: {str(self.sort_type)}")
        self.sort_btn.clicked.connect(self.change_sort)
        self.header_hbox.addWidget(self.sort_btn)

        super().addLayout(self.header_hbox)

    def show_list(self):
        self.task_list = TaskList(self.tasks)
        super().addWidget(self.task_list)

    @QtCore.Slot()
    def change_sort(self):
        # mask the enum index to 0b11, meaning it wraps around after 3,
        # saves two branches and improves readability
        self.sort_type = SortType((self.sort_type.value + 1) & 3)
        
        self.sort_tasks()
        # redraw the TaskList
        self.task_list.clear_list()
        self.task_list.populate_list(self.tasks)

        self.sort_btn.setText(f"Sort by: {str(self.sort_type)}")
    
    def sort_tasks(self):
        # these functions are defined within the function as they are only used in this function
        def sort_name(a: Task, b: Task) -> bool:
            return a.title < b.title
        def sort_class(a: Task, b: Task) -> bool:
            return a.class_name < b.class_name
        def sort_priority(a: Task, b: Task) -> bool:
            return a.priority.value < b.priority.value
        def sort_due_date(a: Task, b: Task) -> bool:
            return a.due_date < b.due_date
        
        def swap(v, i, j):
            v[i], v[j] = v[j], v[i]
        
        # this is effectively an anonymous function
        # is used to compare different fields of the task based on the SortType
        # improves performance and readability
        sort_cmp = sort_name

        match self.sort_type:
            case SortType.NAME:
                sort_cmp = sort_name
            case SortType.CLASS:
                sort_cmp = sort_class
            case SortType.PRIORITY:
                sort_cmp = sort_priority
            case SortType.DUEDATE:
                sort_cmp = sort_due_date
        
        # selection sort
        list_len = len(self.tasks)

        for i in range(0, list_len):
            min_j = i

            for j in range(i + 1, list_len):
                if sort_cmp(self.tasks[j], self.tasks[min_j]):
                    min_j = j
            
            if min_j != i:
                swap(self.tasks, i, min_j)

