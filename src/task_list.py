from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6 import QtGui

from task import *
from utils import *

# ? Data types:
# ?     - Enum: was used for self.sort_type because it can easily represent a finite number of states (such as sorting by name, class, etc)
# ?     - int: used to keep track of the current index when iterating over a list of task cards. This was necessary to check if it should be striped or not (based on if its index was odd or even)
# ?     - str: used to store text that will be displayed to the user in the GUI
# ?     - bool: used because it can only represent a binary on/off state, was used to convey if a task should be striped or not and if task matched a sort comparison
# ?     - TaskCard: represents a single task in the GUI, stores the child GUI widgets used to create the task card in the ui
# ?     - TaskList: represents the scrollable list part of the task list GUI. Acts as a container for the widgets that handle scrolling and the TaskCards
# ?     - TaskView: represents the entire task list GUI, combines the TaskList with a header and handles task sorting
# ? Data Structures:
# ?     - list[Task]: was used because it provides a method of storing Tasks in a way that allows more tasks to be added and sorted

# an enum has been used as the sort type can only be defined as these specific values
# (effectively a constant)
class SortType(IntEnum):
    NAME = 0
    CLASS = 1
    DUEDATE = 2
    PRIORITY = 3

    # override string casting for the button text
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

# represents a single task entry in the task list
class TaskCard(QtWidgets.QFrame):
    selected = QtCore.Signal(Task)

    def __init__(self, task: Task, striped: bool, index: int):
        super().__init__()

        self.index = index
        self.task = task

        hbox = QtWidgets.QHBoxLayout()
        vbox = QtWidgets.QVBoxLayout()

        # initialise labels
        # use html/rich text for text formatting
        title = QtWidgets.QLabel(f"<h3>{task.get_title()}</h3>")
        due_date = QtWidgets.QLabel(f"<p><i><u><b>{task.get_due_date().strftime("%d/%m/%y")}</b></u></i></p>")
        class_name = QtWidgets.QLabel(f"{task.get_class()}") 

        vbox.addWidget(title)
        vbox.addWidget(due_date)
        vbox.addWidget(class_name)

        hbox.addLayout(vbox)

        hbox.addStretch()

        # allows the task to be marked as complete from the task list
        self.checkbox = QtWidgets.QCheckBox()
        self.checkbox.setChecked(task.is_complete())
        self.checkbox.checkStateChanged.connect(self.checkbox_pressed)
        hbox.addWidget(self.checkbox)

        colour = "light" if striped else "window"

        # set style and sizing
        super().setLayout(hbox)
        super().setStyleSheet(f"background-color: palette({colour}); border-radius: 8px;")
        # allows the card to fill horizontal space but not vertical space
        super().setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)

    # mark as complete callback
    def checkbox_pressed(self):
        self.task.set_completed(self.checkbox.isChecked())

    # mouse click callback
    # used to determine if this task card has been selected
    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        # signal to the rest of the program that this task has been selected
        self.selected.emit(self.index)

# represents the scrollable list part of the widget
class TaskList(QtWidgets.QScrollArea):
    def __init__(self, tasks: list[Task], on_task_selected):
        super().__init__()
        # set styling and sizing
        super().setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        super().setWidgetResizable(True)

        self.main_vbox = QtWidgets.QVBoxLayout()
        
        # a blank widget is used to hold the vbox which contains the task cards
        # this widget is set as the primary widget for the qscrollarea
        self.holder_widget = QtWidgets.QWidget()
        self.holder_widget.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)

        # set vbox styling
        self.list_vbox = QtWidgets.QVBoxLayout()
        self.list_vbox.setSpacing(0)
        self.list_vbox.setContentsMargins(0, 0, 0, 0)

        # this pushes all task cards to the top of the task list
        self.list_spacer = QtWidgets.QSpacerItem(
            0, 0,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding
        )

        self.task_cards: list[TaskCard] = []

        # populates the list with task cards based on the list of Task objects
        self.populate_list(tasks, on_task_selected)

        self.holder_widget.setLayout(self.list_vbox)
        super().setWidget(self.holder_widget)
    
    # remove all tasks cards from the widget
    def clear_list(self):
        for card in self.task_cards:
            card.deleteLater()

        self.list_vbox.removeItem(self.list_spacer)
        self.task_cards.clear()
    
    # adds task cards to the list based on a list of task objects
    # assumes task_cards is empty, otherwise duplicates will be created
    def populate_list(self, tasks: list[Task], on_task_selected):
        for i, task in enumerate(tasks):
            # sets the task cards colour based on if it's index is even
            task_card = TaskCard(task, i % 2 == 0, i)
            task_card.selected.connect(self.select_task)
            task_card.selected.connect(on_task_selected)

            self.list_vbox.addWidget(task_card)
            self.task_cards.append(task_card)
        
        self.list_vbox.addSpacerItem(self.list_spacer)

    # sets the colours of all tasks cards to be striped based on their index
    # sets the selected tasks colour to the highlighted colour
    def select_task(self, index: int):
        print("task selected")
        # uses teh tasks index (int) to check if it should be coloured light or not
        for i, task in enumerate(self.task_cards):
            if i == index:
                task.setStyleSheet(f"background-color: palette(accent); border-radius: 8px;")
            else:
                colour = "light" if i % 2 == 0 else "window"
                task.setStyleSheet(f"background-color: palette({colour}); border-radius: 8px;")

# this class combines the TaskList with a header and manages the sorting of tasks
class TaskView(QtWidgets.QVBoxLayout):
    def __init__(self, tasks: list[Task], on_task_selected):
        super().__init__()
        super().setContentsMargins(0, 0, 0, 0)

        # initialise state
        self.on_task_selected = on_task_selected

        self.tasks = tasks
        self.sort_type = SortType.NAME

        # draw ui
        self.show_header()
        self.show_list(on_task_selected)

    # shows the header part of the list, including the title and sort button
    # split from __init__ for readability
    def show_header(self):
        self.header_hbox = QtWidgets.QHBoxLayout()

        self.title = QtWidgets.QLabel('<h2>Tasks</h2>')
        self.header_hbox.addWidget(self.title)

        self.sort_btn = QtWidgets.QPushButton(f"Sort by: {str(self.sort_type)}")
        self.sort_btn.clicked.connect(self.change_sort)
        self.header_hbox.addWidget(self.sort_btn)

        super().addLayout(self.header_hbox)

        self.seperator = SeperatorLine(False)
        
        super().addWidget(self.seperator)

    # shows the TaskList widget
    # spit from __init__ for readability
    def show_list(self, on_task_selected):
        self.task_list = TaskList(self.tasks, on_task_selected)
        super().addWidget(self.task_list)

    # clears and repopulates the task list
    # used when a Task object is changed
    def redraw_list(self):
        self.task_list.clear_list()
        self.task_list.populate_list(self.tasks, self.on_task_selected)

    # callback for the sort button
    # changes the sort type, sorts the tasks and redraws the task list
    def change_sort(self):
        # mask the enum index to 0b11, meaning it wraps around after 3,
        # saves two branches and improves readability
        self.sort_type = SortType((self.sort_type.value + 1) & 3)
        
        # sort tasks and redraw task list
        self.sort_tasks()
        self.redraw_list()

        self.sort_btn.setText(f"Sort by: {str(self.sort_type)}")
    
    # sorts the list of Task objects based on sort_type
    def sort_tasks(self):
        # these functions are defined within the function as they are only used in this function
        # defines the comparison made to sort the list baed on the sort type
        def sort_name(a: Task, b: Task) -> bool:
            return a.title < b.title
        def sort_class(a: Task, b: Task) -> bool:
            return a.class_name < b.class_name
        def sort_priority(a: Task, b: Task) -> bool:
            return a.priority.value < b.priority.value
        def sort_due_date(a: Task, b: Task) -> bool:
            return a.due_date < b.due_date
        
        # swap two elements in a list
        def swap(v, i, j):
            v[i], v[j] = v[j], v[i]
        
        # this is effectively an anonymous function
        # is used to compare different fields of the task based on the SortType
        # improves performance and readability
        sort_cmp = sort_name

        # set the sort_cmp based on the sort_type
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

